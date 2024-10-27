
from .mainClass import *
from .tools     import *

from itertools import zip_longest
import math

class Euclidean(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'
		
	def compute(self,point1: List[float], point2: List[float]) -> float:
		# def distance_function(self,point1, point2):
		"""
		Calculate the Euclidean distance between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:return: Euclidean distance between point1 and point2
		"""
		point1=tuple(point1)
		point2=tuple(point2)
		return math.dist(point1,point2)
		
class L2(Euclidean):
	def __init__(self):
		super().__init__()
		self.type='vec_float'



class InverseTanimoto(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='set_float'


	def compute(self, set_a:set, set_b:set) -> float:
		"""
		Calculate the Inverse Tanimoto coefficient between two sets.

		Parameters:
		- set_a: First set of elements.
		- set_b: Second set of elements.

		Returns:
		- Inverse Tanimoto coefficient: A float value representing the dissimilarity between the two sets.
		"""

		# Calculate the intersection and union of the two sets
		intersection = set_a.intersection(set_b)
		union = set_a.union(set_b)

		# Handle the edge case where the union is empty
		if not union:
			return 0.0

		# Calculate the Inverse Tanimoto coefficient
		inverse_tanimoto = (len(union) - len(intersection)) / len(union)

		return inverse_tanimoto


class Manhattan(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,point1:list, point2:list) -> int:
		"""
		Calculate the Manhattan distance, taxicab or L1 between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:return: Manhattan distance between point1 and point2
		:raises ValueError: If the points are not of the same dimension
		"""  
		distance = sum(abs(p1 - p2) for p1, p2 in zip(point1, point2))
		return distance
		
class L1(Manhattan):
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

class Minkowski(Distance):
	
	def __init__(self, p=3)-> None:
		super().__init__()
		self.type='vec_float'
		self.p=p
		
	def compute(self,point1:list, point2:list) -> float:
		"""
		Calculate the Minkowski distance between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:param p: The order of the Minkowski distance
		:return: Minkowski distance between point1 and point2
		:raises ValueError: If the points are not of the same dimension
		"""
		distance = sum(abs(p1 - p2) ** self.p for p1, p2 in zip(point1, point2)) ** (1 / self.p)
		return distance
		
	def exemple():
		self.obj3_exemple = self.p
		super().exemple()


class Mahalanobis(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='list_list'

	def mean(self,data:list[list]):
		"""
		Calculate the mean of each dimension in the dataset.
    
		:param data: A dataset as a list of points (list of lists)
		:return: Mean of each dimension as a list
		"""
		n = len(data)
		d = len(data[0])
		mean = [0] * d
    
		for point in data:
			for i in range(d):
				mean[i] += point[i]
    
		mean = [x / n for x in mean]
		return mean

	def covariance_matrix(self,data, mean):
		"""
		Calculate the covariance matrix of the dataset.
    
		:param data: A dataset as a list of points (list of lists)
		:param mean: Mean of each dimension as a list
		:return: Covariance matrix as a list of lists
		"""
		n = len(data)
		d = len(data[0])
		cov_matrix = [[0] * d for _ in range(d)]
    
		for point in data:
			diff = [point[i] - mean[i] for i in range(d)]
			for i in range(d):
				for j in range(d):
					cov_matrix[i][j] += diff[i] * diff[j]
    
		cov_matrix = [[x / (n - 1) for x in row] for row in cov_matrix]
		return cov_matrix

	def matrix_inverse(self,matrix):
		"""
		Calculate the inverse of a matrix using Gauss-Jordan elimination.
    
		:param matrix: A square matrix as a list of lists
		:return: Inverse of the matrix as a list of lists
		"""
		n = len(matrix)
		identity = [[float(i == j) for i in range(n)] for j in range(n)]
		augmented = [row + identity_row for row, identity_row in zip(matrix, identity)]
		for i in range(n):
			pivot = augmented[i][i]
			for j in range(2 * n):
				augmented[i][j] /= pivot
			for k in range(n):
				if k != i:
					factor = augmented[k][i]
					for j in range(2 * n):
						augmented[k][j] -= factor * augmented[i][j]
    
		inverse = [row[n:] for row in augmented]
		return inverse

	def compute(self,point :list, data :list[list]) -> float:
		"""
		Calculate the Mahalanobis distance between a point and a dataset.
    
		:param point: A point as a list of coordinates
		:param data: A dataset as a list of points (list of lists)
		:return: Mahalanobis distance between the point and the dataset
		:raises ValueError: If the point dimensions do not match the dataset dimensions
		! lever une execption si la matrice est singulière
		"""
    
		mean_data = self.mean(data)
		cov_matrix = self.covariance_matrix(data, mean_data)
		cov_matrix_inv = self.matrix_inverse(cov_matrix)
    
		diff = [point[i] - mean_data[i] for i in range(len(point))]
    
		# Matrix multiplication: diff^T * cov_matrix_inv * diff
		result = 0
		for i in range(len(diff)):
			for j in range(len(diff)):
				result += diff[i] * cov_matrix_inv[i][j] * diff[j]
    
		return result**0.5
	def exemple(self):
		self.obj2_exemple = [
    [2, 1, 0],
    [2, 3, 4],
    [3, 4, 5],
    [4, 5, 6],
]
		super().exemple()

class RussellRao(Distance):
    def __init__(self )-> None:
        """
        Initialize the Russell-Rao class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        super().__init__()
        self.type='vec_float'

        
    def compute(self,vector1 :list, vector2 :list) -> float:
        """
        Calculate the Russell-Rao distance between the two binary vectors.

        :return: The Russell-Rao distance as a float.
        """
        # Calculate the number of matching features (both present)
        a = sum(v1 and v2 for v1, v2 in zip(vector1, vector2))

        # Calculate the total number of features
        n = len(vector1)

        # Calculate the Russell-Rao distance
        distance = a / n

        return distance
        
class Chebyshev(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,point1 :list, point2 :list) -> float:

		"""
		Calculate the Chebyshev distance between two points.
    
		:param point1: A list of coordinates for the first point
		:param point2: A list of coordinates for the second point
		:return: Chebyshev distance between the two points
		:raises ValueError: If the points do not have the same dimensions
		"""
    
		return max(abs(a - b) for a, b in zip(point1, point2))

'''
class RatcliffObershelp:
    def __init__(self):
        """
        Initialize the Ratcliff/Obershelp class with two strings.

        :param string1: First string for comparison.
        :param string2: Second string for comparison.
        """
        self.string1 = string1
        self.string2 = string2

    def distance_function(self, string1, string2):
        """
        Calculate the Ratcliff/Obershelp distance between the two strings.

        :return: The Ratcliff/Obershelp distance as a float.
        """
        def ratcliff_obershelp(s1, s2):
            if not s1 or not s2:
                return 0.0 if s1 != s2 else 1.0

            def lcs(s1, s2):
                m, n = len(s1), len(s2)
                dp = [[0] * (n + 1) for _ in range(m + 1)]

                for i in range(1, m + 1):
                    for j in range(1, n + 1):
                        if s1[i - 1] == s2[j - 1]:
                            dp[i][j] = dp[i - 1][j - 1] + 1
                        else:
                            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

                return dp[m][n]

            lcs_length = lcs(s1, s2)
            if lcs_length == 0:
                return 0.0

            prefix_length = 0
            while prefix_length < len(s1) and prefix_length < len(s2) and s1[prefix_length] == s2[prefix_length]:
                prefix_length += 1

            similarity = 2 * lcs_length / (len(s1) + len(s2))
            similarity += (2 * prefix_length) / (len(s1) + len(s2))
            return similarity

        similarity = ratcliff_obershelp(self.string1, self.string2)
        return 1 - similarity
'''
class Jaro(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='str'

	def compute(self,s1 :str, s2 :str) -> float:
		"""
		Calculate the Jaro similarity between two strings.
    
		:param s1: The first string
		:param s2: The second string
		:return: Jaro similarity between the two strings
		"""
		if s1 == s2:
			return 1.0

		len_s1 = len(s1)
		len_s2 = len(s2)

		if len_s1 == 0 or len_s2 == 0:
			return 0.0

		match_distance = max(len_s1, len_s2) // 2 - 1

		s1_matches = [False] * len_s1
		s2_matches = [False] * len_s2

		matches = 0
		transpositions = 0

		for i in range(len_s1):
			start = max(0, i - match_distance)
			end = min(i + match_distance + 1, len_s2)

			for j in range(start, end):
				if s2_matches[j]:
					continue
				if s1[i] != s2[j]:
					continue
				s1_matches[i] = True
				s2_matches[j] = True
				matches += 1
				break

		if matches == 0:
			return 0.0

		k = 0
		for i in range(len_s1):
			if not s1_matches[i]:
				continue
			while not s2_matches[k]:
				k += 1
			if s1[i] != s2[k]:
				transpositions += 1
			k += 1

		return (matches / len_s1 + matches / len_s2 + (matches - transpositions // 2) / matches) / 3.0
		
	def exemple(self):
		self.obj1_exemple = "martha"
		self.obj2_exemple = "marhta"
		super().exemple()


class Hausdorff(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='tuple_float'


	def compute(self,set1 :tuple, set2 :tuple) -> float:
		"""
		Calculate the Hausdorff distance between two sets of points.
    
		:param set1: The first set of points, each point represented as a tuple (x, y)
		:param set2: The second set of points, each point represented as a tuple (x, y)
		:return: Hausdorff distance between the two sets of points
		"""
		def max_min_distance(set_a, set_b):
			"""
			Helper function to find the maximum of the minimum distances from each point in set_a to the closest point in set_b.
        
			:param set_a: The first set of points
			:param set_b: The second set of points
			:return: Maximum of the minimum distances
			"""
			max_min_dist = 0
			for point_a in set_a:
				min_dist = float('inf')
				for point_b in set_b:
					dist = Euclidean().calculate(point_a, point_b)
					if dist < min_dist:
						min_dist = dist
				if min_dist > max_min_dist:
					max_min_dist = min_dist
			return max_min_dist

		return max(max_min_distance(set1, set2), max_min_distance(set2, set1))
		
	def exemple(self):
		self.obj1_exemple = [(0, 0), (0, 1), (1, 0), (1, 1)]
		self.obj2_exemple = [(2, 2), (2, 3), (3, 2), (3, 3)]
		super().exemple()


class KendallTau(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_int'

	def compute(self,permutation1 :list[int], permutation2 :list[int]) -> int:
		"""
		Calculate the Kendall Tau distance between two permutations.
    
		:param permutation1: The first permutation (a list of integers)
		:param permutation2: The second permutation (a list of integers)
		:return: Kendall Tau distance between the two permutations
		"""    
		n = len(permutation1)
		pairs = [(permutation1[i], permutation2[i]) for i in range(n)]
    
		def count_inversions(pairs :list):
			"""
			Helper function to count inversions in a list of pairs.
        
			:param pairs: List of pairs
			:return: Number of inversions
			"""
			inversions = 0
			for i in range(len(pairs)):
				for j in range(i + 1, len(pairs)):
					if (pairs[i][0] > pairs[j][0] and pairs[i][1] < pairs[j][1]) or (pairs[i][0] < pairs[j][0] and pairs[i][1] > pairs[j][1]):
						inversions += 1
			return inversions

		return count_inversions(pairs)
		



class Haversine(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,p1 :list,p2 :list ) -> float:
		"""
		Calculate the Haversine distance between two points on the Earth's surface.
    
		:param lat1: Latitude of the first point in decimal degrees
		:param lon1: Longitude of the first point in decimal degrees
		:param lat2: Latitude of the second point in decimal degrees
		:param lon2: Longitude of the second point in decimal degrees
		:return: Haversine distance between the two points in kilometers
		"""
		lat1, lon1=p1[0],p1[1]
		lat2, lon2=p2[0],p2[1]
		# Radius of the Earth in kilometers
		R = 6371.0
    
		# Convert latitude and longitude from degrees to radians
		lat1_rad = degrees_to_radians(lat1)
		lon1_rad = degrees_to_radians(lon1)
		lat2_rad = degrees_to_radians(lat2)
		lon2_rad = degrees_to_radians(lon2)
    
		# Differences in coordinates
		dlat = lat2_rad - lat1_rad
		dlon = lon2_rad - lon1_rad
    
		# Haversine formula
		a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
		c = 2 * atan2(a**0.5, (1 - a)**0.5)
    
		# Distance in kilometers
		distance = R * c
    
		return distance
		
	def exemple(self):
		self.obj1_exemple = (48.8566, 2.3522)# Paris coordinates
		self.obj2_exemple = (51.5074, -0.1278)# London coordinates
		super().exemple()

class Canberra(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,point1 :list, point2 :list) -> float:
		"""
		Calculate the Canberra distance between two points.
    
		:param point1: The first point (a list of numerical values)
		:param point2: The second point (a list of numerical values)
		:return: Canberra distance between the two points
		"""    
		distance = 0
		for x1, x2 in zip(point1, point2):
			numerator = abs(x1 - x2)
			denominator = abs(x1) + abs(x2)
			if denominator != 0:
				distance += numerator / denominator
    
		return distance

class BrayCurtis(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,point1 :list, point2 :list) -> float:
		"""
		Calculate the Bray-Curtis distance between two points.
    
		:param point1: The first point (a list of numerical values)
		:param point2: The second point (a list of numerical values)
		:return: Bray-Curtis distance between the two points
		"""
    
		sum_diff = 0
		sum_sum = 0
    
		for x1, x2 in zip(point1, point2):
			sum_diff += abs(x1 - x2)
			sum_sum += abs(x1 + x2)
    
		if sum_sum == 0:
			return 0  # To handle the case when both points are zeros
    
		distance = sum_diff / sum_sum
		return distance


class Matching(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_bin'

	def compute(self,seq1 :list, seq2 :list) -> int:
		"""
		Calculate the Matching (Hamming) distance between two sequences.
    
		:param seq1: The first sequence (a list or string of characters or binary values)
		:param seq2: The second sequence (a list or string of characters or binary values)
		:return: Matching distance between the two sequences
		"""
    
		distance = sum(el1 != el2 for el1, el2 in zip(seq1, seq2))
    
		return distance



class Kulsinski(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='set_float'

	def compute(self,set1 :set, set2 :set) -> float:
		"""
		Calculate the Kulsinski distance between two sets or binary vectors.
    
		:param set1: The first set (a set of elements or a list of binary values)
		:param set2: The second set (a set of elements or a list of binary values)
		:return: Kulsinski distance between the two sets or binary vectors
		"""
		if isinstance(set1, set) and isinstance(set2, set):
			# Calculate for sets
			intersection = len(set1.intersection(set2))
			union = len(set1.union(set2))
			a = intersection
			b = len(set1) - intersection
			c = len(set2) - intersection
			d = union - a - b - c
		elif isinstance(set1, list) and isinstance(set2, list):
			# Calculate for binary vectors
			a = sum(1 for x, y in zip(set1, set2) if x == 1 and y == 1)
			b = sum(1 for x, y in zip(set1, set2) if x == 1 and y == 0)
			c = sum(1 for x, y in zip(set1, set2) if x == 0 and y == 1)
			d = sum(1 for x, y in zip(set1, set2) if x == 0 and y == 0)

		n = a + b + c + d
    
		return (b + c - a + n) / (b + c + n)
		
	def exemple(self):
		self.obj1_exemple = {"a", "b", "c", "d"}
		self.obj2_exemple = {"b", "c", "e", "f"}

		super().exemple()




class Yule(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_bin'

	def compute(self,binary_vector1 :list[int], binary_vector2 :list[int]) -> float:
		"""
		Calcule la distance de Yule entre deux vecteurs binaires.
    
		:param binary_vector1: Premier vecteur binaire (liste de 0 et 1)
		:param binary_vector2: Deuxième vecteur binaire (liste de 0 et 1)
		:return: Distance de Yule
		"""
    
		# Calcul des variables a, b, c, d
		a = b = c = d = 0
    
		for bit1, bit2 in zip(binary_vector1, binary_vector2):
			if bit1 == 1 and bit2 == 1:
				a += 1
			elif bit1 == 1 and bit2 == 0:
				b += 1
			elif bit1 == 0 and bit2 == 1:
				c += 1
			elif bit1 == 0 and bit2 == 0:
				d += 1
    
		# Calcul de l'indice de dissimilarité de Yule Q
		if (a * d + b * c) == 0:
			return 0.0  # Si le dénominateur est 0, la dissimilarité est 0 (vecteurs identiques)
    
		Q = 2 * b * c / (a * d + b * c)
        
		return Q / (Q + 2 * a * d)
		
	#def exemple(self):
	#	self.obj1_exemple =  [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
	#	self.obj2_exemple = [0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
	#	super().exemple()



class Bhattacharyya(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,P :list[float], Q :list[float]) -> float:
		"""
		Calcule la distance de Bhattacharyya entre deux distributions de probabilité discrètes.
    
		:param P: Première distribution de probabilité (liste de probabilités)
		:param Q: Deuxième distribution de probabilité (liste de probabilités)
		:return: Distance de Bhattacharyya
		"""
    
		# Calcul du coefficient de Bhattacharyya
		bc = 0.0
		for p, q in zip(P, Q):
			bc += (p * q)**0.5
    
		# Calcul de la distance de Bhattacharyya
		distance = -log(bc)
    
		return distance


class Gower(Distance):
	
	def __init__(self,ranges=None)-> None:
		super().__init__()
		self.type='vec_float_str'

		self.ranges=ranges
	def compute(self, vec1 :list, vec2 :list) -> float:
		"""
		Calculate the Gower similarity between two vectors.

		Parameters:
		- vec1: List of values for the first entity (can include both numerical and categorical).
		- vec2: List of values for the second entity (can include both numerical and categorical).
		- ranges: List of ranges for numerical variables. Use `None` for categorical variables.

		Returns:
		- Similarity: Gower similarity between vec1 and vec2.
		"""

		total_similarity = 0
		num_variables = len(vec1)

		for i in range(num_variables):
			if self.ranges[i] is None:
				# Categorical variable
				if vec1[i] == vec2[i]:
					similarity = 1
				else:
				    similarity = 0
			else:
				# Numerical variable
				if vec1[i] == vec2[i]:
					similarity = 1
				else:
					range_value = self.ranges[i]
					if range_value == 0:
						similarity = 0
					else:
						similarity = 1 - abs(vec1[i] - vec2[i]) / range_value

			total_similarity += similarity

		# Normalize by the number of variables
		return total_similarity / num_variables
		
	def exemple(self):
		test_cases = [
			(["Red", 3.2, 5], ["Blue", 4.1, 3], [None, 5.0, 10]),
			([5.5, "M", 200], [6.1, "F", 180], [10, None, 50]),
			([0, "High", 10], [1, "Low", 10], [1, None, 10]),
			([100, "Yes", 3.5], [150, "No", 2.8], [50, None, 5]),
			([1.5, "Green", 2], [1.5, "Green", 2], [None, None, None])
		]

		# Compute and print the Gower similarity for each pair
		for vec1, vec2, ranges in test_cases:
			similarity = gower.calculate(vec1, vec2, ranges)
			print(f"Gower similarity between {vec1} and {vec2}: {similarity:.4f}")

class Hellinger(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_prob'


	def compute(self,p :list[float], q :list[float]) -> float:
		"""
		Calcule la distance de Hellinger entre deux distributions de probabilités.
    
		:param p: Première distribution de probabilités (sous forme de liste ou d'array).
		:param q: Deuxième distribution de probabilités (sous forme de liste ou d'array).
		:return: Distance de Hellinger entre p et q.
		"""
    
		# Calculer la distance de Hellinger
		sum_of_squares = sum(((p_i)**0.5 - (q_i)**0.5 ) ** 2 for p_i, q_i in zip(p, q))
    
		return (1 / 2**0.5 ) * sum_of_squares**0.5

class CzekanowskiDice(Distance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_int'

	def compute(self,x :list, y :list) -> float:
		"""
		Calcule la distance Czekanowski-Dice entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:return: Distance Czekanowski-Dice entre x et y.
		"""
    
		min_sum = sum(min(x_i, y_i) for x_i, y_i in zip(x, y))
		sum_x = sum(x)
		sum_y = sum(y)
    
		if sum_x + sum_y == 0:
			return 0.0  # Pour éviter la division par zéro
    
		dice_similarity = (2 * min_sum) / (sum_x + sum_y)
    
		return 1 - dice_similarity

class Wasserstein(Distance) :
	
    def __init__(self)-> None:
        """
        Initialize the Wasserstein class with two probability distributions.

        :param distribution1: First probability distribution (list of floats).
        :param distribution2: Second probability distribution (list of floats).
        """
        super().__init__()
        self.type='vec_prob'


    def compute(self, distribution1 :list, distribution2 :list)-> float:
        """
        Calculate the Wasserstein distance between the two distributions.

        :return: The Wasserstein distance as a float.
        """
    
        # Cumulative distribution functions (CDF) of both distributions
        cdf1 = self._cumulative_distribution(distribution1)
        cdf2 = self._cumulative_distribution(distribution2)

        # Wasserstein distance is the area between the CDFs
        distance = sum(abs(c1 - c2) for c1, c2 in zip(cdf1, cdf2))

        return distance

    def _cumulative_distribution(self, distribution :list[float]):
        """
        Calculate the cumulative distribution for a given distribution.

        :param distribution: A probability distribution (list of floats).
        :return: The cumulative distribution (list of floats).
        """
        cdf = []
        cumulative_sum = 0.0
        for prob in distribution:
            cumulative_sum += prob
            cdf.append(cumulative_sum)
        return cdf



