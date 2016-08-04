# -*- coding: utf-8 -*-
r"""
Databases and accessors of online databases for coding theory
"""

def best_linear_code_in_guava(n, k, F):
    r"""
    Returns the best linear code of length ``n``, dimension ``k`` over field
    ``F`` that is known to the GAP package GUAVA.

    The function uses the tables described in ``bounds_on_minimum_distance_in_guava`` to
    construct this code. This requires the optional GAP package GUAVA.

    EXAMPLES::

        sage: sage.coding.databases.best_linear_code_in_guava(10,5,GF(2))    # long time; optional - gap_packages (Guava package)
        Linear code of length 10, dimension 5 over Finite Field of size 2
        sage: gap.eval("C:=BestKnownLinearCode(10,5,GF(2))")     # long time; optional - gap_packages (Guava package)
        'a linear [10,5,4]2..4 shortened code'

    This means that the best possible binary linear code of length 10 and
    dimension 5 is a code with minimum distance 4 and covering radius s somewhere
    between 2 and 4. Use ``bounds_on_minimum_distance_in_guava(10,5,GF(2))``
    for further details.
    """
    q = F.order()
    C = gap("BestKnownLinearCode(%s,%s,GF(%s))"%(n,k,q))
    G = C.GeneratorMat()
    k = G.Length()
    n = G[1].Length()
    Gs = G._matrix_(F)
    MS = MatrixSpace(F,k,n)
    return LinearCode(MS(Gs))



def bounds_on_minimum_distance_in_guava(n, k, F):
    r"""
    Computes a lower and upper bound on the greatest minimum distance of a
    `[n,k]` linear code over the field ``F``.

    This function requires the optional GAP package GUAVA.

    The function returns a GAP record with the two bounds and an explanation for
    each bound. The function Display can be used to show the explanations.

    The values for the lower and upper bound are obtained from a table
    constructed by Cen Tjhai for GUAVA, derived from the table of
    Brouwer. See http://www.codetables.de/ for the most recent data.
    These tables contain lower and upper bounds for `q=2` (when ``n <= 257``),
    `q=3` (when ``n <= 243``), `q=4` (``n <= 256``). (Current as of
    11 May 2006.) For codes over other fields and for larger word lengths,
    trivial bounds are used.

    The format of the output is a GAP record object. See below for an example.

    EXAMPLES::

        sage: print(bounds_minimum_distance(10,5,GF(2))) # optional - gap_packages (Guava package)
        rec(
          construction :=
           [ <Operation "ShortenedCode">,
              [
                  [ <Operation "UUVCode">,
                      [
                          [ <Operation "DualCode">,
                              [ [ <Operation "RepetitionCode">, [ 8, 2 ] ] ] ],
                          [ <Operation "UUVCode">,
                              [
                                  [ <Operation "DualCode">,
                                      [ [ <Operation "RepetitionCode">, [ 4, 2 ] ] ] ]
                                    , [ <Operation "RepetitionCode">, [ 4, 2 ] ] ] ]
                         ] ], [ 1, 2, 3, 4, 5, 6 ] ] ],
          k := 5,
          lowerBound := 4,
          lowerBoundExplanation := ...
          n := 10,
          q := 2,
          references := rec(
               ),
          upperBound := 4,
          upperBoundExplanation := ... )
    """
    q = F.order()
    gap.eval("data := BoundsMinimumDistance(%s,%s,GF(%s))"%(n,k,q))
    Ldata = gap.eval("Display(data)")
    return Ldata




def best_linear_code_in_codetables_dot_de(n, k, F, verbose=False):
    r"""
    Return the best linear code and its construction as per the web database
    http://codetables.de.

    INPUT:

    -  ``n`` - Integer, the length of the code

    -  ``k`` - Integer, the dimension of the code

    -  ``F`` - Finite field, of order 2, 3, 4, 5, 7, 8, or 9

    -  ``verbose`` - Bool (default: ``False``)

    OUTPUT:

    -  An unparsed text explaining the construction of the code.

    EXAMPLES::

        sage: L = best_known_linear_code_www(72, 36, GF(2)) # optional - internet
        sage: print(L)                                      # optional - internet
        Construction of a linear code
        [72,36,15] over GF(2):
        [1]:  [73, 36, 16] Cyclic Linear Code over GF(2)
             CyclicCode of length 73 with generating polynomial x^37 + x^36 + x^34 +
        x^33 + x^32 + x^27 + x^25 + x^24 + x^22 + x^21 + x^19 + x^18 + x^15 + x^11 +
        x^10 + x^8 + x^7 + x^5 + x^3 + 1
        [2]:  [72, 36, 15] Linear Code over GF(2)
             Puncturing of [1] at 1
        <BLANKLINE>
        last modified: 2002-03-20

    This function raises an ``IOError`` if an error occurs downloading data or
    parsing it. It raises a ``ValueError`` if the ``q`` input is invalid.

    AUTHORS:

    - Steven Sivek (2005-11-14)
    - David Joyner (2008-03)
    """
    from six.moves.urllib.request import urlopen
    q = F.order()
    if not q in [2, 3, 4, 5, 7, 8, 9]:
        raise ValueError("q (=%s) must be in [2,3,4,5,7,8,9]"%q)
    n = int(n)
    k = int(k)

    param = ("?q=%s&n=%s&k=%s"%(q,n,k)).replace('L','')

    url = "http://iaks-www.ira.uka.de/home/grassl/codetables/BKLC/BKLC.php"+param
    if verbose:
        print("Looking up the bounds at %s" % url)
    f = urlopen(url)
    s = f.read()
    f.close()

    i = s.find("<PRE>")
    j = s.find("</PRE>")
    if i == -1 or j == -1:
        raise IOError("Error parsing data (missing pre tags).")
    text = s[i+5:j].strip()
    return text



def self_orthogonal_binary_codes(n, k, b=2, parent=None, BC=None, equal=False,
    in_test=None):
    """
    Returns a Python iterator which generates a complete set of
    representatives of all permutation equivalence classes of
    self-orthogonal binary linear codes of length in ``[1..n]`` and
    dimension in ``[1..k]``.

    INPUT:

    -  ``n`` - Integer, maximal length

    -  ``k`` - Integer, maximal dimension

    -  ``b`` - Integer, requires that the generators all have weight divisible
       by ``b`` (if ``b=2``, all self-orthogonal codes are generated, and if
       ``b=4``, all doubly even codes are generated). Must be an even positive
       integer.

    -  ``parent`` - Used in recursion (default: ``None``)

    -  ``BC`` - Used in recursion (default: ``None``)

    -  ``equal`` - If ``True`` generates only [n, k] codes (default: ``False``)

    -  ``in_test`` - Used in recursion (default: ``None``)

    EXAMPLES:

    Generate all self-orthogonal codes of length up to 7 and dimension up
    to 3::

        sage: for B in self_orthogonal_binary_codes(7,3):
        ....:    print(B)
        Linear code of length 2, dimension 1 over Finite Field of size 2
        Linear code of length 4, dimension 2 over Finite Field of size 2
        Linear code of length 6, dimension 3 over Finite Field of size 2
        Linear code of length 4, dimension 1 over Finite Field of size 2
        Linear code of length 6, dimension 2 over Finite Field of size 2
        Linear code of length 6, dimension 2 over Finite Field of size 2
        Linear code of length 7, dimension 3 over Finite Field of size 2
        Linear code of length 6, dimension 1 over Finite Field of size 2

    Generate all doubly-even codes of length up to 7 and dimension up
    to 3::

        sage: for B in self_orthogonal_binary_codes(7,3,4):
        ....:    print(B); print(B.generator_matrix())
        Linear code of length 4, dimension 1 over Finite Field of size 2
        [1 1 1 1]
        Linear code of length 6, dimension 2 over Finite Field of size 2
        [1 1 1 1 0 0]
        [0 1 0 1 1 1]
        Linear code of length 7, dimension 3 over Finite Field of size 2
        [1 0 1 1 0 1 0]
        [0 1 0 1 1 1 0]
        [0 0 1 0 1 1 1]

    Generate all doubly-even codes of length up to 7 and dimension up
    to 2::

        sage: for B in self_orthogonal_binary_codes(7,2,4):
        ....:    print(B); print(B.generator_matrix())
        Linear code of length 4, dimension 1 over Finite Field of size 2
        [1 1 1 1]
        Linear code of length 6, dimension 2 over Finite Field of size 2
        [1 1 1 1 0 0]
        [0 1 0 1 1 1]

    Generate all self-orthogonal codes of length equal to 8 and
    dimension equal to 4::

        sage: for B in self_orthogonal_binary_codes(8, 4, equal=True):
        ....:     print(B); print(B.generator_matrix())
        Linear code of length 8, dimension 4 over Finite Field of size 2
        [1 0 0 1 0 0 0 0]
        [0 1 0 0 1 0 0 0]
        [0 0 1 0 0 1 0 0]
        [0 0 0 0 0 0 1 1]
        Linear code of length 8, dimension 4 over Finite Field of size 2
        [1 0 0 1 1 0 1 0]
        [0 1 0 1 1 1 0 0]
        [0 0 1 0 1 1 1 0]
        [0 0 0 1 0 1 1 1]

    Since all the codes will be self-orthogonal, b must be divisible by
    2::

        sage: list(self_orthogonal_binary_codes(8, 4, 1, equal=True))
        Traceback (most recent call last):
        ...
        ValueError: b (1) must be a positive even integer.
    """
    d=int(b)
    if d!=b or d%2==1 or d <= 0:
        raise ValueError("b (%s) must be a positive even integer."%b)
    from .binary_code import BinaryCode, BinaryCodeClassifier
    if k < 1 or n < 2:
        return
    if equal:
        in_test = lambda M : (M.ncols() - M.nrows()) <= (n-k)
        out_test = lambda C : (C.dimension() == k) and (C.length() == n)
    else:
        in_test = lambda M : True
        out_test = lambda C : True
    if BC is None:
        BC = BinaryCodeClassifier()
    if parent is None:
        for j in xrange(d, n+1, d):
            M = Matrix(GF(2), [[1]*j])
            if in_test(M):
                for N in self_orthogonal_binary_codes(n, k, d, M, BC, in_test=in_test):
                    if out_test(N): yield N
    else:
        C = LinearCode(parent)
        if out_test(C): yield C
        if k == parent.nrows():
            return
        for nn in xrange(parent.ncols()+1, n+1):
            if in_test(parent):
                for child in BC.generate_children(BinaryCode(parent), nn, d):
                    for N in self_orthogonal_binary_codes(n, k, d, child, BC, in_test=in_test):
                        if out_test(N): yield N

from sage.coding.self_dual_codes import self_dual_binary_codes
