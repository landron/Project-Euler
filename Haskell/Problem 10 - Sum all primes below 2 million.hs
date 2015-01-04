{-
	http://projecteuler.net/problem=10
		Problem 10. Sum all primes below N million
	Version: 2015.01.04

	https://projecteuler.net/profile/landron.png

	for performance measurements:
		:set +s
-}

{-
TODO:	
	1. understand the magic of the trace lines
		'|' => it first evaluates the 'trace'
		why returning False => to skip executing the implementation (undefined)
-}
import Debug.Trace
import qualified Data.Map as Map
import qualified Data.Vector as Vec
import Control.Monad.ST
import qualified Data.Vector.Mutable as MutableVec

assert :: Monad a => Bool -> a ()
assert False = error "assertion failed!"
assert _     = return ()

--You only need to start crossing out multiples at p^2, because any 
--smaller multiple of p has a prime divisor less than p and has already 
--been crossed out as a multipleof that.
get_primes_limit :: Int -> Int
get_primes_limit limit = 1 + floor (sqrt $ fromIntegral limit)
get_primes_limit_old limit = (limit `quot` 3)

--------------------------------------------------------
--1. list of not primes:	too slow for 100000 already

--merge sieve prime next limit | trace ("merge " ++ show sieve ++ " " ++ show next) False = undefined
merge [] prime next limit  	= [next+0*prime, next+2*prime .. limit-1]
merge (x:xs) prime next limit	
	| next >= limit = x:xs
	| x < next 		= x : merge xs prime next limit
	| x == next 	= x : merge xs prime (next+2*prime) limit
	| otherwise 	= next : merge (x:xs) prime (next+2*prime) limit

--3*prime : the prime number was already added
gen_sieve sieve prime limit = merge sieve prime (3*prime) limit

--primes_sum_rec sieve sum current limit | trace ("primes_sum_rec " ++ show sieve ++ " " ++ show sum ++ " " ++ show current) False = undefined
--primes_sum_rec sieve sum current limit | trace ("primes_sum_rec " ++ show sieve ++ " " ++ show current) False = undefined
primes_sum_rec [] sum_now current limit = sum_now + sum [current, current + 2 .. limit-1]
primes_sum_rec sieve sum current limit
	| current >= limit = sum
	| current == head sieve = primes_sum_rec (tail sieve) sum (current + 2) limit
	| otherwise = primes_sum_rec (gen_sieve (dropWhile (<current+2) sieve) current limit) (sum + current) (current + 2) limit

primes_sum1 limit = primes_sum_rec [2] 2 3 limit

--------------------------------------------------------
--2. list of primes

update_next_prime1 current prime next
	| next == current = next+2*prime
	| otherwise = next
update_sieve1 current db = Map.mapWithKey (update_next_prime1 current) db

find_prime_update_sieve current found prime next
	| next == current = (True, next+2*prime)
	| otherwise = (found, next)
find_update_sieve current db = Map.mapAccumWithKey (find_prime_update_sieve current) False db

update_sieve2 current sum db
	| fst next = (snd next, sum)
	| otherwise = (Map.insert current (3*current) db, sum+current)
	where next = find_update_sieve current db

calculate_primes_sum_rec current limit sum db
	| current >= limit = sum
	| otherwise = calculate_primes_sum_rec (2+current) limit (snd next) (fst next)
	where next = update_sieve2 current sum db

calculate_primes_sum limit = calculate_primes_sum_rec 3 limit 2 Map.empty
primes_sum2 = calculate_primes_sum

--------------------------------------------------------
--3. very large array

--update_sieve_step prime db limit = db Vec.// [(i,0) | i <- [3*prime, 5*prime .. limit-1]]
update_sieve_step prime db limit = Vec.unsafeUpd db [(i,0) | i <- [3*prime, 5*prime .. limit-1]]

--version 1
update_sieve3_rec_1 prime db limit
	| prime == 2 = update_sieve3_rec 3 (Vec.unsafeUpd db [(i,0) | i <- [4,6 .. limit-1]]) limit
	| prime <= (get_primes_limit limit) = update_sieve3_rec (prime+2) (update_sieve_step prime db limit) limit
	| otherwise = db
update_sieve3_1 limit = update_sieve3_rec_1 2 (Vec.generate limit (id)) limit

--version 2: not really faster than the previous one
update_sieve3_rec prime db limit
	| prime <= (get_primes_limit limit) = update_sieve3_rec (prime+2) (update_sieve_step prime db limit) limit
	| otherwise = db
update_sieve3_first db limit = update_sieve3_rec 3 (Vec.unsafeUpd db [(i,0) | i <- [4,6 .. limit-1]]) limit
update_sieve3_2 limit = update_sieve3_first (Vec.generate limit (id)) limit

update_sieve3 = update_sieve3_1
primes_sum3 limit = Vec.sum (update_sieve3 limit) - 1

--------------------------------------------------------
--4. very large mutable array: the solution

update_sieve4_step_M 2 limit arr = do
	mapM_ (\i -> MutableVec.write arr i 0) [4, 6 .. limit-1]
update_sieve4_step_M prime limit arr = do
	mapM_ (\i -> MutableVec.write arr i 0) [3*prime, 5*prime .. limit-1]

update_sieve4_step limit arrIn = do
	arr <- Vec.unsafeThaw arrIn
	MutableVec.write arr 1 0
	update_sieve4_step_M 2 limit arr
	mapM_ (\p -> update_sieve4_step_M p limit arr) [3, 5 .. get_primes_limit limit]
	Vec.unsafeFreeze arr

update_sieve4 limit = update_sieve4_step limit (Vec.generate limit (id))

--TODO: can't get this out of the monad (not m Int); print does it somehow
primes_sum4_1 limit = do 
	sieve <- update_sieve4 limit
	return (Vec.sum sieve)

primes_sum4 limit = runST $ do primes_sum4_1 limit

--------------------------------------------------------
--------------------------------------------------------
--------------------------------------------------------
--main

{-
*Main> :set +s

25000
	*Main> print $ primes_sum2 25000
	32405717
	(25.13 secs, 8957734352 bytes)

	*Main> print $ primes_sum1 25000
	32405717
	(17.63 secs, 2932785248 bytes)

	*Main> primes_sum3 25000
	32405717
	(3.54 secs, 877852024 bytes)

	*Main> primes_sum4 25000
	32405717
	(0.09 secs, 0 bytes)

100000
	*Main> primes_sum3 100000
	454396537
	(68.52 secs, 13454883256 bytes)

	*Main> primes_sum4 100000
	454396537
	(0.31 secs, 128253128 bytes)

200000
	*Main> primes_sum3 200000
	1709600813
	(285.83 secs, 53613163952 bytes)

	*Main> primes_sum4 200000
	1709600813
	(0.66 secs, 268875688 bytes)

2000000
	*Main> primes_sum4 2000000
	142913828922
	(12.25 secs, 3193954912 bytes)

	the new get_primes_limit version
	*Main> primes_sum4 2000000
	142913828922
	(5.09 secs, 1368733064 bytes)
-}

validate = do
	--primes_sum1
	assert (17 == primes_sum1 9)
	assert (17 == primes_sum1 10)
	assert (17 == primes_sum1 11)
	assert (28 == primes_sum1 12)
	assert (100 == primes_sum1 29)
	assert (129 == primes_sum1 30)
	assert (1060 == primes_sum1 100)
	assert (76127 == primes_sum1 1000)
	assert (True || 5736396 == primes_sum1 10000)
	
	--primes_sum2
	assert (17 == primes_sum2 9)
	assert (17 == primes_sum2 10)
	assert (17 == primes_sum2 11)
	assert (28 == primes_sum2 12)
	assert (100 == primes_sum2 29)
	assert (129 == primes_sum2 30)
	assert (1060 == primes_sum2 100)
	assert (76127 == primes_sum2 1000)
	assert (True || 5736396 == primes_sum2 10000)
	assert (True || 32405717 == primes_sum2 25000)

	--primes_sum3
	assert (17 == primes_sum3 9)
	assert (17 == primes_sum3 10)
	assert (17 == primes_sum3 11)
	assert (28 == primes_sum3 12)
	assert (100 == primes_sum3 29)
	assert (129 == primes_sum3 30)
	assert (1060 == primes_sum3 100)
	assert (76127 == primes_sum3 1000)
	assert (5736396 == primes_sum3 10000)
	assert (True || 32405717 == primes_sum3 25000)
	assert (True || 454396537 == primes_sum3 100000)

	--primes_sum4
	assert (17 == primes_sum4 9)
	assert (17 == primes_sum4 10)
	assert (17 == primes_sum4 11)
	assert (28 == primes_sum4 12)
	assert (100 == primes_sum4 29)
	assert (129 == primes_sum4 30)
	assert (1060 == primes_sum4 100)
	assert (76127 == primes_sum4 1000)
	assert (5736396 == primes_sum4 10000)
	assert (32405717 == primes_sum4 25000)
	assert (454396537 == primes_sum4 100000)
	assert (False || 142913828922 == primes_sum4 2000000)	

	putStrLn "Validation done!"

main = do
	--print $ primes_sum3 200000
	print $ primes_sum4 2000000