import unittest
import time

from typing import List, Tuple
Point = Tuple[int, int]

# Generic tree node class 
class TreeNode(object): 
    def __init__(self, val): 
        self.val = val 
        self.left = None
        self.right = None
       


class OrthogonalRangeSearch():



    def __init__(self, canvas):
        self.width = canvas.winfo_width()
        self.height = canvas.winfo_height()

        print("width: ", self.width)
        print("height: ", self.height)
    # orthogonalRangeSearch --------------------------------------------------------------------------------------------
    # main function for input to the problem, takes in a list of points and a range, utilizes recurseBuildKDTree to build
    # a kdTree with the given points. It then uses recuseSearchKDTree to find the points within the range
    # Input: points: List[Point], targetRange, canvas(tkinter)
    #
    # Modifies --> canvas
    # Returns  --> KDTree Object containg every point in points

    def orthogonalRangeSearch(self, points, targetRange, canvas):

        infRegion = ((-float("inf"),float("inf")),(-float("inf"), float("inf")))

        kdRoot = self.recurseBuildKDTree(points, 0, canvas, infRegion)
        ans = []

        infRegion = ((-float("inf"),float("inf")),(-float("inf"), float("inf")))

        self.recurseSearchKDTree(kdRoot, infRegion, targetRange, ans)
        return sorted(ans)


    # recurseBuildKDTree --------------------------------------------------------------------------------------------
    # A recursive algorithm to build a 2 dimensional KD tree given a set of points. First called with depth 0
    # Input: points: List[Point], depth: int, canvas(tkinter)
    #
    # Modifies --> None
    # Returns  --> TreeNode Object at root of KDTree containing every point in points
    def recurseBuildKDTree(self, points: List[Point], depth: int, canvas, currentRegion):
    

        time.sleep(.1)
        # Base Case
        if len(points) == 0: 
            return None
        if len(points) == 1:
            return TreeNode(points[0])



        print(currentRegion)

        leftChildRegion, rightChildRegion = None, None

        # 2 Cases, on even depth split points with a vertical lines, on odd depth split with a horizonal line
        if depth % 2 == 0:
            
            # Split points into two subests with a vertical line through the median x-coordinate of the points.
            # p1 will be points to the left or on l, while p2 will be points to the right of l
            dir = "v"
            points = sorted(points) #TODO: Implement faster version of this
            median = self.getMedian(points, 0)
            canvas.create_line(int(median), max(0,currentRegion[1][0]), int(median), min(self.height, currentRegion[1][1]))
            canvas.update_idletasks

            p1 = [point for point in points if point[0] <= median]
            p2 = [point for point in points if point[0] > median]

            leftChildRegion = ( (currentRegion[0][0], median) , (currentRegion[1][0], currentRegion[1][1]) )
            rightChildRegion = ( (median,currentRegion[0][1]) , (currentRegion[1][0], currentRegion[1][1]) )
       
        

        else:
            
            # Split points into two subests with a horizontal line through the median y-coordinate of the points.
            # p1 will be points to the below or on l, while p2 will be points to the above of l
            dir = "h"
            points = sorted(points, key = lambda x: x[1]) #TODO: Implement faster version of this
            median = self.getMedian(points, 1)
            canvas.create_line( max(0, currentRegion[0][0]), int(median), min(self.width, currentRegion[0][1]), int(median))
            canvas.update_idletasks

            p1 = [point for point in points if point[1] <= median]
            p2 = [point for point in points if point[1] > median]

            leftChildRegion = ( (currentRegion[0][0], currentRegion[0][1]) , (currentRegion[1][0], median) )
            rightChildRegion = ( (currentRegion[0][0], currentRegion[0][1]) , (median, currentRegion[1][1]) )

        # Recursively call function to create subtrees
        leftChild = self.recurseBuildKDTree(p1, depth + 1, canvas, leftChildRegion)
        rightChild = self.recurseBuildKDTree(p2, depth + 1, canvas, rightChildRegion)

        # Create node representing the separating line

        newNode = TreeNode((median, dir))
        newNode.left = leftChild
        newNode.right = rightChild

        return newNode

    # recurseSearchKDTree -----------------------------------------------------------------------------------------
    # A recursive algorithm that searches a kdTree for points that fall in the targetRegion specified, 
    # regions are repesented as a tuple of tuples ((x:x'),(y:y')) with x and x' being the right and left boundaries of the region
    # current region should be initiated with [(-float("inf"), float("inf")), (-float("inf"), float("inf"))]]
    #
    # Modifies --> None
    # Returns  --> set of points from the kdTree in targetRegion
    
    def recurseSearchKDTree(self, node : TreeNode, currentRegion, targetRegion, output: List[Point]):
        

        if node == None: return
        # print(" NODE: ", node.val, "node.left: ", node.left.val, "node.right: ", node.right.val)
        # If node is a leaf then report that point if it lies in R
        if node.left == None and node.right == None:
            if targetRegion[0][0] <= node.val[0] <= targetRegion[0][1] and targetRegion[1][0] <= node.val[1] <= targetRegion[1][1]:
                output.append(node.val)
            return

        leftChildRegion, rightChildRegion = None, None
       
        # Determine the region of the left child node from the current region and the median
        if node.val[1] == "v":
            leftChildRegion = ( (currentRegion[0][0], node.val[0]) , (currentRegion[1][0], currentRegion[1][1]) )
            rightChildRegion = ( (node.val[0],currentRegion[0][1]) , (currentRegion[1][0], currentRegion[1][1]) )
        elif node.val[1] == "h":
            leftChildRegion = ( (currentRegion[0][0], currentRegion[0][1]) , (currentRegion[1][0], node.val[0]) )
            rightChildRegion = ( (currentRegion[0][0], currentRegion[0][1]) , (node.val[0], currentRegion[1][1]) )

   
        

        # if region of left child is fully contained in target region
        if self.containsRegion(targetRegion, leftChildRegion):
            # Report all leaves in the subtree, (Add them to the output array)
            self.reportSubTree(node.left, output)

        # Else if region of left child intersects target region
        elif self.regionsIntersect(targetRegion, leftChildRegion):  
            #recurseSearchKDTree(lc(node)
            self.recurseSearchKDTree(node.left, leftChildRegion, targetRegion, output)



        

        
        # if region of right child is fully contained in target region
        if self.containsRegion(targetRegion, rightChildRegion):
            # Report all leaves in the subtree, (Add them to the output array)
            self.reportSubTree(node.right, output)

        # Else if region of right child intersects target region
        elif self.regionsIntersect(targetRegion, rightChildRegion):      
            #recurseSearchKDTree(rc(node)
            self.recurseSearchKDTree(node.right, rightChildRegion, targetRegion, output)





    # reportSubTree --------------------------------------------------------------------------------------------
    # Adds all points in this subtree to the output list provided
    #  
    # Modifies --> output
    # Returns --> None
    def reportSubTree(self, root, output):
        if root == None:
            return

        self.reportSubTree(root.left, output)

        # If node is a leaf add it to the output array
        if root.left == None and root.right == None:
            output.append(root.val)

        self.reportSubTree(root.right, output)




    # containsRegion --------------------------------------------------------------------------------------------
    # takes 2 regions as input, returns True if region1 contains region2, False otherwise
    # regions are repesented as a tuple of tuples ((x:x'),(y:y')) with x and x' being the right and left boundaries of the region
    #
    # Modifies --> None
    # Output --> True/False

    def containsRegion(self, region1, region2):

        if region1[0][0] <= region2[0][0] and region1[0][1] >= region2[0][1] and  region1[1][0] <= region2[1][0] and  region1[1][1] >= region2[1][1]:
            return True
        return False 



    # regionsIntersect --------------------------------------------------------------------------------------------
    # takes 2 regions as input, returns True if the two regions intersect, False otherwise
    # regions are repesented as a tuple of tuples ((x:x'),(y:y')) with x and x' being the right and left boundaries of the region
    #
    # Modifies --> None
    # Output --> True/False

    def regionsIntersect(self, region1, region2):

        if region2[0][0] > region1[0][1] or region1[0][0] > region2[0][1]:
            return False

        if region2[1][0] > region1[1][1] or region1[1][0] > region2[1][1]:
            return False

        return True

  

    # getMedian --------------------------------------------------------------------------------------------
    # Returns the median value of a given list of points assuming that they are sorted, takes a flag representing if the x or y value should be used
    # a 0 represents x and 1 represents y
    # Input --> List[Points], int
    #
    # Modifies --> None
    # Returns  --> float

    def getMedian(self, points, x):
        return ( points[int(len(points) / 2)][x] + points[int((len(points) -1) / 2)][x] ) / 2


class TestOrthogonalRangeSearch(unittest.TestCase):

    

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
        self.assertEqual(inOrder, [(1,1), (3.0, "v"), (5,3), (3.0,"h"), (2,4), (6.5,"v"), (8,7), (8.5,"v"), (9,10), (10.0,"h"), (40,30)], "recurseBuildKDTree() Failed")

    

    def test_recurseSearchKDTree(self):


        ORS = OrthogonalRangeSearch()

        testPoints = [(1,1),(2,4),(5,3),(8,7),(9,10),(40,30)]

        testTree = ORS.recurseBuildKDTree(testPoints, 0)
        testRegion = ( (2,9), (1,7))
        output = []
        infRegion = ((-float("inf"),float("inf")),(-float("inf"), float("inf")))

        ORS.recurseSearchKDTree(testTree, infRegion, testRegion, output)

        output.sort()

        self.assertEqual( output, [(2,4),(5,3),(8,7)],"recurseSearchKDTree() Failed")




    def test_containsRegion(self):
        ORS = OrthogonalRangeSearch()
        self.assertEqual( ORS.containsRegion( ((1,10),(5, 9)), ((2,10),(6, 8)) ), True, "containsRegion() Failed")
        self.assertEqual( ORS.containsRegion( ((1,10),(5, 9)), ((1,10),(5, 9)) ), True, "containsRegion() Failed")
        self.assertEqual( ORS.containsRegion( ((2,10),(5, 9)), ((1,10),(5, 9)) ), False, "containsRegion() Failed")
        self.assertEqual( ORS.containsRegion( ((2,10),(6, 9)), ((1,10),(5, 9)) ), False, "containsRegion() Failed")
        self.assertEqual( ORS.containsRegion( ((-float("inf"),float("inf")),(-float("inf"), float("inf"))), ((2,10),(6, 8)) ), True, "containsRegion() Failed")
        self.assertEqual( ORS.containsRegion( ((-float("inf"),11),(-float("inf"), float("inf"))), ((2,10),(6, 8)) ), True, "containsRegion() Failed")

    def test_regionsIntersect(self):
        ORS = OrthogonalRangeSearch()
        self.assertEqual( ORS.regionsIntersect( ((1,10),(5, 9)), ((2,10),(6, 8)) ), True, "regionsIntersect() Failed")
        self.assertEqual( ORS.regionsIntersect( ((1,10),(5, 9)), ((5,15),(1, 6)) ), True, "regionsIntersect() Failed")
        self.assertEqual( ORS.regionsIntersect( ((2,10),(5, 9)), ((1,10),(5, 9)) ), True, "regionsIntersect() Failed")
        self.assertEqual( ORS.regionsIntersect( ((2,10),(2, 10)), ((40,50),(40, 50)) ), False, "regionsIntersect() Failed")
        self.assertEqual( ORS.regionsIntersect( ((3,6.5),(-float("inf"), 3)), ((2,9),(1, 7)) ), True, "regionsIntersect() Failed")
        self.assertEqual( ORS.regionsIntersect( ( (2,9),(1, 7) ), ( (3,6.5) , (-float("inf"), 3) )), True, "regionsIntersect() Failed")


    def test_orthogonalRangeSearch(self):

        ORS = OrthogonalRangeSearch()
        points1 = [(1,1),(2,4),(5,3),(8,7),(9,10),(40,30)]
        region1 = ((2,9), (1,7))
        self.assertEqual(ORS.orthogonalRangeSearch(points1, region1), [(2,4),(5,3),(8,7)], "orthogonalRangeSearch() Failed")


        points2 = [(1,1),(2,4),(5,3),(8,7),(9,10),(40,30),(2,1),(9,7)]
        region2 = ((2,9), (1,7))
        self.assertEqual(ORS.orthogonalRangeSearch(points2, region2), [(2,1),(2,4),(5,3),(8,7),(9,7)], "orthogonalRangeSearch() Failed")

        points3 = [(-5,9),(-8,5),(9,1000),(0,0),(5,4),(15, 354), (5,20), (30, 25), (41.02, 43)]
        region3 = ((-7,41.05), (1,44))
        self.assertEqual(ORS.orthogonalRangeSearch(points3, region3), [(-5,9),(5,4),(5,20),(30,25), (41.02, 43)], "orthogonalRangeSearch() Failed")


if __name__ == '__main__':
    unittest.main()