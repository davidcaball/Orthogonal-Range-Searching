import unittest



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
			return TreeNode(points[0])

		# 2 Cases, on even depth split points with a vertical lines, on odd depth split with a horizonal line
		if depth % 2 == 0:
			# Split points into two subests with a vertical line through the median x-coordinate of the points.
			# p1 will be points to the left or on l, while p2 will be points to the right of l
			
			points = sorted(points) #TODO: Implement faster version of this
			median = self.getMedian(points, 0)
			p1 = [point for point in points if point[0] <= median]
			p2 = [point for point in points if point[0] > median]
		
		else:
			# Split points into two subests with a horizontal line through the median y-coordinate of the points.
			# p1 will be points to the below or on l, while p2 will be points to the above of l
			
			points = sorted(points, key = lambda x: x[1]) #TODO: Implement faster version of this
			median = self.getMedian(points, 1)

			p1 = [point for point in points if point[1] <= median]
			p2 = [point for point in points if point[1] > median]

		# Recursively call function to create subtrees
		leftChild = self.recurseBuildKDTree(p1, depth + 1)
		rightChild = self.recurseBuildKDTree(p2, depth + 1)

		# Create node representing the separating line
		newNode = TreeNode(median)
		newNode.left = leftChild
		newNode.right = rightChild

		return newNode


	# recurseSearchKDTree ------------------------------------------------------------------------------------------
	# A recursive algorithm that searches a kdTree for points that fall in the region specified
	# Modifies --> None
	# Returns  --> set of points from the kdTree in region
	
	def searchKDTree(self, kdTree : TreeNode, region):
		print("TODO")




	def sortPoints(self, points: List[Point]) -> Tuple[List[Point],List[Point]]:
		xSort = sorted(points)
		ySort = sorted(points, key = lambda x: x[1])

		return (xSort, ySort)

	



	# getMedian --------------------------------------------------------------------------------------------
	# Returns the median value of a given list of points assuming that they are sorted, takes a flag representing if the x or y value should be used
	# a 0 represents x and 1 represents y
	# Input --> List[Points], int
	#
	# Modifies --> None
	# Returns  --> float

	def getMedian(self, points, x) -> float:
		return ( points[int(len(points) / 2)][x] + points[int((len(points) -1) / 2)][x] ) / 2


class TestOrthogonalRangeSearch(unittest.TestCase):

    def test_sortPoints(self):
        ORS = OrthogonalRangeSearch()
        res = ORS.sortPoints( [(-1,4),(4,6),(2,-8),(122,43),(0,3),(-123,-54)] )
        self.assertEqual(res[0] , [(-123, -54), (-1, 4), (0, 3), (2, -8), (4, 6), (122, 43)], "sortPoints Failed")
        self.assertEqual(res[1] , [(-123, -54), (2, -8), (0, 3), (-1, 4), (4, 6), (122, 43)], "sortPoints Failed")

    def test_getMedian(self):
    	ORS = OrthogonalRangeSearch()
    	self.assertEqual(ORS.getMedian( [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)] , 0) , 4, "getMedian() Failed")
    	self.assertEqual(ORS.getMedian( [(1,1),(2,2),(3,3),(4,4),(5,5),(5,5),(6,6),(7,7)], 1) , 4.5, "getMedian() Failed")
    


    def test_recurseBuildKDTree(self):

    	# Takes the root node of a tree and modifies the result List to represent an in order traversal of the tree
    	def inOrderTraversal(root: TreeNode, result: List):
    		if root:
    			inOrderTraversal(root.left, result)
    			result.append(root.val)
    			inOrderTraversal(root.right, result)

    	ORS = OrthogonalRangeSearch()
    	testPoints = [(1,1),(2,4),(5,3),(8,7),(9,10),(40,30)]
    	testTree = ORS.recurseBuildKDTree(testPoints, 0)
    	inOrder = []
    	inOrderTraversal(testTree, inOrder)
    	self.assertEqual(inOrder, [(1,1), 3.0, (5,3), 3.0, (2,4), 6.5, (8,7), 8.5, (9,10), 10.0, (40,30)], "recurseBuildKDTree() Failed")





if __name__ == '__main__':
	unittest.main()