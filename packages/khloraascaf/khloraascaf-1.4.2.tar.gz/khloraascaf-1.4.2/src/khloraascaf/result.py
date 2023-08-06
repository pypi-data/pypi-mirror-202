# -*- coding=utf-8 -*-

"""Caffolding result's module: structures and utils."""


from __future__ import annotations

from collections.abc import Iterable, Iterator
from queue import LifoQueue, Queue
from typing import Optional, Union

from pulp import LpProblem
from revsymg.index_lib import FORWARD_INT, REVERSE_INT, IndexT, OrT

from khloraascaf.exceptions import NotACircuit
from khloraascaf.ilp.dirf_sets import dirf_canonical, dirf_other
from khloraascaf.ilp.invf_sets import invf_canonical, invf_other
from khloraascaf.ilp.pulp_var_db import (
    BIN_THRESHOLD,
    PuLPVarDirFModel,
    PuLPVarInvFModel,
    PuLPVarModelT,
)
from khloraascaf.lib import DR_CODE, IR_CODE, SC_CODE, RegionCodeT
from khloraascaf.multiplied_doubled_contig_graph import (
    COCC_IND,
    COR_IND,
    MDCGraph,
    OccOrCT,
)


# ============================================================================ #
#                                     TYPES                                    #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                Genomic Regions                               #
# ---------------------------------------------------------------------------- #
OrRegT = tuple[IndexT, OrT]
OrRegMapT = tuple[OrRegT, ...]
RegOccOrCT = tuple[OccOrCT, ...]
#
# Builder
#
_OrRegMapT = list[OrRegT]
_RegOccOrCT = list[OccOrCT]
#
# LifoQueue and Queue
#
RepQueueT = dict[IndexT, Union[LifoQueue[OccOrCT], Queue[OccOrCT]]]


# ============================================================================ #
#                                     CLASS                                    #
# ============================================================================ #
# pylint: disable=too-many-instance-attributes
class ScaffoldingResult():
    """Scaffolding result class.

    An instance contains a genomic regions map and each genomic regions'
    oriented contigs.

    Warning
    -------
    You must not call the constructor, you must only deal with the objects
    that have been already instanced.
    You can use the class name to type your variables.
    """

    # DOCU update docstring
    # DOCU add to docstring example to get regions' orc from result

    # pylint: disable=too-many-arguments
    def __init__(self, ilp_codes: tuple[RegionCodeT, ...],
                 status: int, opt_value: float,
                 region_map: OrRegMapT,
                 regions_occorc: tuple[RegOccOrCT, ...],
                 sc_regions: tuple[IndexT, ...],
                 ir_regions: tuple[IndexT, ...],
                 dr_regions: tuple[IndexT, ...]):
        """The Initializer."""
        #
        # Ilp origin
        #
        self.__ilp_codes: tuple[RegionCodeT, ...] = ilp_codes
        #
        # ILP result
        #
        self.__status: int = status
        self.__opt_value: float = opt_value
        #
        # Genomic region
        #
        self.__region_map: OrRegMapT = region_map
        self.__regions_occorc: tuple[RegOccOrCT, ...] = regions_occorc
        self.__sc_regions: tuple[IndexT, ...] = sc_regions
        self.__ir_regions: tuple[IndexT, ...] = ir_regions
        self.__dr_regions: tuple[IndexT, ...] = dr_regions

    # ~*~ Getter ~*~

    def last_ilp(self) -> RegionCodeT:
        """Return last ILP code.

        Returns
        -------
        RegionCodeT
            Last ILP code
        """
        return self.__ilp_codes[-1]

    def ilp_codes(self) -> Iterator[RegionCodeT]:
        """Iterate over ILP codes.

        Yields
        ------
        RegionCodeT
            ILP code
        """
        yield from self.__ilp_codes

    def status(self) -> int:
        """Returns status code.

        Returns
        -------
        int
            Status code
        """
        return self.__status

    def opt_value(self) -> float:
        """ILP optimal value.

        Returns
        -------
        float
            ILP optimal value
        """
        return self.__opt_value

    def map_of_regions(self) -> Iterator[tuple[IndexT, OrT]]:
        """Iterate over the regions and their orientation.

        Yields
        ------
        IndexT
            Region's index
        OrT
            Region's orientation
        """
        yield from self.__region_map

    def region_occorc(self, region_index: IndexT) -> Iterator[OccOrCT]:
        """Iterate over the multiplied oriented contigs of the region.

        Parameters
        ----------
        region_index : IndexT
            Region's index

        Yields
        ------
        OccOrCT
            Multiplied oriented contig of the region
        """
        yield from self.__regions_occorc[region_index]

    def number_regions(self) -> int:
        """Returns the number of regions.

        Returns
        -------
        int
            Number of regions
        """
        return len(self.__regions_occorc)

    def sc_regions(self) -> Iterator[IndexT]:
        """Iterate over the single copy indices.

        Yields
        ------
        IndexT
            Single copy region index
        """
        yield from self.__sc_regions

    def ir_regions(self) -> Iterator[IndexT]:
        """Iterate over inverted repeat indices.

        Yields
        ------
        IndexT
            Inverted repeats index
        """
        yield from self.__ir_regions

    def dr_regions(self) -> Iterator[IndexT]:
        """Iterate over direct repeat indices.

        Yields
        ------
        IndexT
            Direct repeats index
        """
        yield from self.__dr_regions


class _ScaffoldingResultBuilder():
    """The scaffolding result builder."""

    __NO_OPT_VALUE = .0

    @classmethod
    def __fix_opt_value(cls, prob: LpProblem) -> float:
        """Fix the #XXX PuLP issue 331.

        Parameters
        ----------
        prob : LpProblem
            PuLP problem

        Returns
        -------
        float
            Optimal value
        """
        if prob.objective.value() is not None:
            return prob.objective.value()
        return cls.__NO_OPT_VALUE

    def __init__(self):
        """The Initializer."""
        #
        # Genomic region
        #
        self.__region_map: _OrRegMapT = []
        self.__regions_occorc: list[_RegOccOrCT] = []
        self.__sc_regions: list[IndexT] = []
        self.__ir_regions: list[IndexT] = []
        self.__dr_regions: list[IndexT] = []

    # ~*~ Setter ~*~

    def add_region(self,
                   region_code: RegionCodeT,
                   region_index: Optional[IndexT] = None) -> IndexT:
        """Add a region.

         # XXX region_index provides the first repeat
         * this works because we build pair of repeated regions

        Parameters
        ----------
        region_code : RegionCodeT
            Region code
        region_index : IndexT, optional
            Index of an already existing region, else None

        Returns
        -------
        IndexT
            Region's index
        """
        #
        # Non-existing region
        #
        if region_index is None:
            region_index = len(self.__regions_occorc)
            self.__regions_occorc.append([])
            self.__region_map.append((region_index, FORWARD_INT))
            if region_code == IR_CODE:
                self.__ir_regions.append(region_index)
            elif region_code == DR_CODE:
                self.__dr_regions.append(region_index)
            else:
                self.__sc_regions.append(region_index)
        #
        # Already existing region (repeat)
        #
        else:
            if region_code == IR_CODE:
                self.__region_map.append((region_index, REVERSE_INT))
            elif region_code == DR_CODE:
                self.__region_map.append((region_index, FORWARD_INT))
        return region_index

    def add_occorc_to_region(self, v: OccOrCT, region_index: IndexT):
        """Add v to the region denoted by its index.

        Parameters
        ----------
        v : OccOrCT
            Multiplied oriented contig
        region_index : IndexT
            Region's index
        """
        self.__regions_occorc[region_index].append(v)

    # ~*~ Getter ~*~

    def view(self, prob: LpProblem,
             ilp_codes: Iterable[RegionCodeT]) -> ScaffoldingResult:
        """Return a ScaffoldingResult view from the builder.

        Parameters
        ----------
        prob : LpProblem
            PuLP problem
        ilp_codes : iterable of RegionCodeT
            ILP codes

        Returns
        -------
        ScaffoldingResult
            Scaffolding result view
        """
        return ScaffoldingResult(
            tuple(ilp_codes),
            prob.status,
            self.__fix_opt_value(prob),
            tuple(self.__region_map),
            tuple(tuple(regoccorc) for regoccorc in self.__regions_occorc),
            tuple(self.__sc_regions),
            tuple(self.__ir_regions),
            tuple(self.__dr_regions),
        )


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                               Build The Regions                              #
# ---------------------------------------------------------------------------- #
# pylint: disable=too-many-arguments
def path_to_regions(mdcg: MDCGraph, starter_vertex: OccOrCT,
                    ilp_codes: Iterable[RegionCodeT],
                    prob: LpProblem, var: PuLPVarModelT,
                    fix_result: Optional[ScaffoldingResult] = None) -> (
                        ScaffoldingResult):
    """Extract regions from optimal path.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    ilp_codes : iterable of RegionCodeT
        Code of the regions that have been scaffolded
    prob : LpProblem
        PuLP problem
    var : PuLPVarModelT
        PuLP variables
    fix_result : ScaffoldingResult, optional
        Scaffolding result with regions, by default `None`

    Returns
    -------
    ScaffoldingResult
        Scaffolding result
    """
    # REFACTOR should path_to_regions be a method for result builder?
    # ------------------------------------------------------------------------ #
    # Manage paired fragments
    # ------------------------------------------------------------------------ #
    set_invf_paired = __create_set_invf_paired(var, fix_result)
    set_dirf_paired = __create_set_dirf_paired(var, fix_result)

    # ------------------------------------------------------------------------ #
    # Init regions
    # ------------------------------------------------------------------------ #
    result_builder = _ScaffoldingResultBuilder()
    prev_region_code = SC_CODE
    region_index = result_builder.add_region(SC_CODE)

    initial_vertex = __find_initial(
        mdcg, starter_vertex, var, set_invf_paired, set_dirf_paired)

    u: OccOrCT = initial_vertex  # previous v
    v: Optional[OccOrCT] = initial_vertex
    #
    # Region IR: LIFO, DR: FIFO
    #
    # XXX no order between pairs of repeats
    #   * for the moment, the pairs of contiguous repeat are not considered
    #       ordered (e.g. pairs of contiguous IR should be lifo, DR fifo)
    rep_queue: RepQueueT = {}
    #
    # Canonical to the region's index: repeat was discovered
    #
    v_canonical_rep: dict[OccOrCT, IndexT] = {}

    # ------------------------------------------------------------------------ #
    # Walk into the solution path
    # ------------------------------------------------------------------------ #
    while v is not None:
        region_code = __get_region_code(v, set_invf_paired, set_dirf_paired)
        #
        # Single-copy
        #
        if region_code == SC_CODE:
            #
            # New single-copy
            #
            if prev_region_code != region_code:
                region_index = result_builder.add_region(region_code)
            result_builder.add_occorc_to_region(v, region_index)
        #
        # IR and DR
        #
        else:
            canonical_repf = (
                invf_canonical(v) if region_code == IR_CODE
                else dirf_canonical(v)
            )
            #
            # First region of the repeat
            #
            if canonical_repf not in v_canonical_rep:
                if not __is_repeat_contiguous(
                        u, v, var, prev_region_code, region_code):
                    region_index = result_builder.add_region(region_code)
                    v_canonical_rep[canonical_repf] = region_index
                    rep_queue[region_index] = (
                        LifoQueue() if region_code == IR_CODE
                        else Queue()
                    )
                __extend_first_rep(
                    region_code, region_index,
                    v, canonical_repf,
                    rep_queue, v_canonical_rep,
                    result_builder,
                )
            #
            # Seconde region of the repeat
            #
            else:
                if not __is_repeat_contiguous(
                        u, v, var, prev_region_code, region_code):
                    region_index = v_canonical_rep[canonical_repf]
                    result_builder.add_region(region_code, region_index)
                assert v == rep_queue[region_index].get()

        prev_region_code = region_code
        u = v
        v = __succ_in_path(v, mdcg, var, initial_vertex)

    # ------------------------------------------------------------------------ #
    # To view
    # ------------------------------------------------------------------------ #
    return result_builder.view(prob, ilp_codes)


def __extend_first_rep(region_code: RegionCodeT, region_index: IndexT,
                       v: OccOrCT, canonical_repf: OccOrCT,
                       rep_queue: RepQueueT,
                       v_canonical_rep: dict[OccOrCT, IndexT],
                       result_builder: _ScaffoldingResultBuilder):
    result_builder.add_occorc_to_region(v, region_index)
    if region_code == IR_CODE:
        rep_queue[region_index].put(invf_other(v))
    elif region_code == DR_CODE:
        rep_queue[region_index].put(dirf_other(v))
    v_canonical_rep[canonical_repf] = region_index


# ---------------------------------------------------------------------------- #
#                               Walk In The Path                               #
# ---------------------------------------------------------------------------- #
def __pred_in_path(v: OccOrCT, mdcg: MDCGraph,
                   var: PuLPVarModelT, initial_vertex: OccOrCT) -> (
        Optional[OccOrCT]):
    """Return the predecessor of vertex v in solution path.

    Stop if the predecessor is the initial vertex.

    Parameters
    ----------
    v : OccOrCT
        Vertex
    mdcg : MDCGraph
        Multiplied doubled contig graph
    var : PuLPVarModelT
        PuLP variables
    initial_vertex : OccOrCT
        Starter vertex

    Returns
    -------
    OccOrCT, optional
        The previous vertex in solution path, None if it is the
        initial vertex

    Raises
    ------
    NotACircuit
        If the path is not a circuit
    """
    for u in mdcg.multiplied_preds(v):
        if var.x[u, v].varValue > BIN_THRESHOLD:
            if u == initial_vertex:
                return None
            return u
    raise NotACircuit()


def __succ_in_path(v: OccOrCT, mdcg: MDCGraph,
                   var: PuLPVarModelT, initial_vertex: OccOrCT) -> (
        Optional[OccOrCT]):
    """Return the successor of vertex v in solution path.

    Stop if the successor is the initial vertex.

    Parameters
    ----------
    v : OccOrCT
        Vertex
    mdcg : MDCGraph
        Multiplied doubled contig graph
    var : PuLPVarModelT
        PuLP variables
    initial_vertex : OccOrCT
        Starter vertex

    Returns
    -------
    OccOrCT, optional
        The next vertex in solution path, None if it is the
        initial vertex

    Raises
    ------
    NotACircuit
        If the path is not a circuit
    """
    for w in mdcg.multiplied_succs(v):
        if var.x[v, w].varValue > BIN_THRESHOLD:
            if w == initial_vertex:
                return None
            return w
    raise NotACircuit()


# ---------------------------------------------------------------------------- #
#                                Initialisation                                #
# ---------------------------------------------------------------------------- #
def __create_set_invf_paired(var: PuLPVarModelT,
                             fix_result: Optional[ScaffoldingResult]) -> (
        set[OccOrCT]):
    """Create set of canonical of paired inverted fragments.

    Parameters
    ----------
    var : PuLPVarModelT
        PuLP variables
    fix_result : ScaffoldingResult, optional
        Scaffolding result, by default `None`

    Returns
    -------
    set of OccOrCT
        Set of canonical of paired inverted fragments
    """
    set_invf_paired: set[OccOrCT] = set()
    #
    # Add old inverted fragments pairing
    #
    if fix_result is not None:
        for region_index in fix_result.ir_regions():
            for v in fix_result.region_occorc(region_index):
                set_invf_paired.add(invf_canonical(v))
    #
    # Add new inverted fragments pairing
    #
    if isinstance(var, PuLPVarInvFModel):
        for invf_sol in var.invf_solution():
            set_invf_paired.add(invf_sol[FORWARD_INT])
    return set_invf_paired


def __create_set_dirf_paired(var: PuLPVarModelT,
                             fix_result: Optional[ScaffoldingResult]) -> (
        set[OccOrCT]):
    """Create set of canonical of paired direct fragments.

    Parameters
    ----------
    var : PuLPVarModelT
        PuLP variables
    fix_result : ScaffoldingResult, optional
        Scaffolding result, by default `None`

    Returns
    -------
    set of OccOrCT
        Set of canonical of paired direct fragments
    """
    set_dirf_paired: set[OccOrCT] = set()
    #
    # Add old direct fragments pairing
    #
    if fix_result is not None:
        for region_index in fix_result.dr_regions():
            for v in fix_result.region_occorc(region_index):
                set_dirf_paired.add(dirf_canonical(v))
    #
    # Add new direct fragments pairing
    #
    if isinstance(var, PuLPVarDirFModel):
        for dirf_sol in var.dirf_solution():
            set_dirf_paired.add(dirf_sol[FORWARD_INT])
    return set_dirf_paired


# pylint: disable=too-many-arguments
def __find_initial(mdcg: MDCGraph, starter_vertex: OccOrCT,
                   var: PuLPVarModelT,
                   set_invf_paired: set[OccOrCT],
                   set_dirf_paired: set[OccOrCT]) -> OccOrCT:
    """The first vertex of the starter's region.

    In case of circular single copy region, it returns starter_vertex.

    Parameters
    ----------
    mdcg : MDCGraph
        Multiplied doubled contig graph
    starter_vertex : OccOrCT
        Starter vertex
    var : PuLPVarModelT
        PuLP variables
    set_invf_paired : set of OccOrCT
        Set of canonical of paired inverted fragments
    set_dirf_paired : set of OccOrCT
        Set of canonical of paired direct fragments

    Returns
    -------
    OccOrCT
        The first vertex of the starter's region
    """
    v: OccOrCT = starter_vertex
    u: Optional[OccOrCT] = __pred_in_path(
        starter_vertex, mdcg, var, starter_vertex)
    # pylint: disable=compare-to-zero
    while (u is not None
           and __get_region_code(u, set_invf_paired, set_dirf_paired) == 0
           ):
        v = u
        u = __pred_in_path(v, mdcg, var, starter_vertex)
    if u is None:
        return starter_vertex
    return v


# ---------------------------------------------------------------------------- #
#                               Region Management                              #
# ---------------------------------------------------------------------------- #
def __get_region_code(v: OccOrCT, set_invf_paired: set[OccOrCT],
                      set_dirf_paired: set[OccOrCT]) -> RegionCodeT:
    """Get the code of the region for the multiplied oriented contig.

    Parameters
    ----------
    v : OccOrCT
        Multiplied oriented contig
    set_invf_paired : set of OccOrCT
        Set of canonical of paired inverted fragments
    set_dirf_paired : set of OccOrCT
        Set of canonical of paired direct fragments

    Returns
    -------
    RegionCodeT
        Code of the region (0: SC; 1: IR; 2: DR)
    """
    if dirf_canonical(v) in set_dirf_paired:
        return DR_CODE
    if ((v[COCC_IND] - v[COR_IND]) % 2 == 0  # pylint: disable=compare-to-zero
            and invf_canonical(v) in set_invf_paired):
        return IR_CODE
    return SC_CODE


def __is_repeat_contiguous(u: OccOrCT, v: OccOrCT, var: PuLPVarModelT,
                           prev_region_code: RegionCodeT,
                           region_code: RegionCodeT) -> bool:
    """Answer yes if the repeat given by its code is contiguous.

    Parameters
    ----------
    u : OccOrCT
        Multiplied oriented contig
    v : OccOrCT
        Multiplied oriented contig
    var : PuLPVarModelT
        PuLP variables
    prev_region_code : RegionCodeT
        Previous region's code
    region_code : RegionCodeT
        Current region's code

    Returns
    -------
    bool
        True if repeat is contiguous, else False
    """
    if prev_region_code != region_code:
        return False
    #
    # IR:
    #   i (= u) -> k(= v): ok, so is there l -> j?
    #
    if region_code == IR_CODE:
        return var.x[invf_other(v), invf_other(u)].varValue > BIN_THRESHOLD
    #
    # DR:
    #   i (= u) -> k(= v): ok, so is there j -> l?
    #
    if region_code == DR_CODE:
        return var.x[dirf_other(u), dirf_other(v)].varValue > BIN_THRESHOLD
    # TODO error out of code
    return False
