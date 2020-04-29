import unittest
from avl import TreeNode, AVL_Tree


from typing import List, Tuple
Point = Tuple[int, int]

# Generic tree node class 
class TreeNode(object): 
    def __init__(self, val): 
        self.val = val 
        self.left = None
        self.right = None
       


class OrthogonalRangeSearch():


	# recurseBuildKDTree --------------------------------------------------------------------------------------------
	# A recursive algorithm to build a 2 dimensional KD tree given a set of points. First called with depth 0
	# Input: points: List[Point], depth: int
	#
	# Modifies --> None
	# Returns  --> KDTree Object containg every point in points
	def recurseBuildKDTree(self, points: List[Point], depth: int) -> TreeNode:
	

		# Base Case
		if len(points) == 0: 
			return None
		if len(points) == 1:
			return TreeNode(point[0])

		# 2 Cases, on even depth split points with a vertical lines, on odd depth split with a horizonal line
		if depth % 2 == 0:
			# Split points into two subests with a vertical line through the median x-coordinate of the points.
			# p1 will be points to the left or on l, while p2 will be points to the right of l
			
			points = sorted(points) #TODO: Implement faster version of this
			median = self.getMedian(sortedPoints)
			p1 = [point for point in points if point[0] <= median]
			p2 = [point for point in points if point[0] > median]
		
		else:
			# Split points into two subests with a horizontal line through the median y-coordinate of the points.
			# p1 will be points to the below or on l, while p2 will be points to the above of l
			
			points = sorted(points, key = lambda x: x[1]) #TODO: Implement faster version of this
			median = self.getMedian(sortedPoints)

			p1 = [point for point in points if point[1] <= median]
			p2 = [point for point in points if point[1] > median]

		# Recursively call function to create subtrees
		leftChild = resurseBuildKDTree(p1, depth + 1)
		rightChild = recurseBuildKDTree(p2, depth + 1)

		# Create node representing the separating line
		newNode = TreeNode(median)
		newNode.left = leftChild
		newNode.right = rightChild

		return newNode


	# recurseSearchKDTree --------------------------------------------------------------------------------------------
	# A recursive algorithm that searches a kdTree for points that fall in the region specified
	#
	# Modifies --> None
	# Returns  --> set of points from the kdTree in region
	def searchKDTree(self, kdTree : TreeNode, region):





	def sortPoints(self, points: List[Point]) -> Tuple[List[Point],List[Point]]:
		xSort = sorted(points)
		ySort = sorted(points, key = lambda x: x[1])

		return (xSort, ySort)

	



	# getMedian --------------------------------------------------------------------------------------------
	# Simply returns the median value of a given list of points assuming that they are sorted
	# Input --> List[Points]
	#
	# Modifies --> None
	# Returns  --> float
	def getMedian(self, points) -> float:
		return ( points[int(len(points) / 2)] + points[int((len(points) -1) / 2)] ) / 2


class TestOrthogonalRangeSearch(unittest.TestCase):

    def test_sortPoints(self):
        ORS = OrthogonalRangeSearch()
        res = ORS.sortPoints( [(-1,4),(4,6),(2,-8),(122,43),(0,3),(-123,-54)] )
        self.assertEqual(res[0] , [(-123, -54), (-1, 4), (0, 3), (2, -8), (4, 6), (122, 43)], "sortPoints Failed")
        self.assertEqual(res[1] , [(-123, -54), (2, -8), (0, 3), (-1, 4), (4, 6), (122, 43)], "sortPoints Failed")

    def test_getMedian(self):
    	ORS = OrthogonalRangeSearch()
    	self.assertEqual(ORS.getMedian([1,2,3,4,5,6,7]) , 4, "getMedian() Failed")
    	self.assertEqual(ORS.getMedian([1,2,3,4,5,5,6,7]) , 4.5, "getMedian() Failed")
    	self.assertEqual(ORS.getMedian([1,2]) , 1.5, "getMedian() Failed")





if __name__ == '__main__':
	unittest.main()