--Problem 9 : Special Pythagorean triplet
--    http://projecteuler.net/problem=9
--        There exists exactly one Pythagorean triplet for which a + b + c = 1000.
--    Version: 2015.01.03

assert :: Monad a => Bool -> a ()
assert False = error "assertion failed!"
assert _     = return ()

is_Pythagorean_triplet a b c = (b < c) && (a^2 + b^2 == c^2)

--The straightforward approach:   the main problem is that the time complexity is quadratic
--    There are better solutions (see the overview of the problem) using mathematical properties of this kind of numbers
find_Pythagorean_triplet sum = [[a,b,sum-a-b] | a <- [1..sum `quot` 3], b <- [a+1..2*sum `quot` 3], is_Pythagorean_triplet a b (sum-a-b)]

find_triplet sum = print $ find_Pythagorean_triplet sum

main = do
    let test = head $ find_Pythagorean_triplet 12
    assert (3 == (test !! 0) && 4 == (test !! 1) && 5 == (test !! 2))
    let test = head $ find_Pythagorean_triplet 30
    assert (5 == (test !! 0) && 12 == (test !! 1) && 13 == (test !! 2))
    let test = head $ find_Pythagorean_triplet 70
    assert (20 == (test !! 0) && 21 == (test !! 1) && 29 == (test !! 2))
    let result = head $ find_Pythagorean_triplet 1000
    assert (200 == (result !! 0) && 375 == (result !! 1) && 425 == (result !! 2))
    assert (31875000 == product result)