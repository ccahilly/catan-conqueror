from board import *


class EdgeTests:
	"""
	Class: Edge
	--------------------------
	A class containing all tests for the Edge class.
	--------------------------
	"""

	def __init__(self):
		pass

	def testEdgeInit(self):
		"""
		Method: testEdgeInit
		--------------------------
		Tests to make sure all instance variables are properly
		initialized.
		--------------------------
		"""
		print "Running testEdgeInit....."

		e1 = Edge(1, 2)
		assert(e1.X is 1)
		assert(e1.Y is 2)
		assert(e1.player is None)

		e1 = Edge(1, 2, 5)
		assert(e1.X is 1)
		assert(e1.Y is 2)
		assert(e1.player is 5)

		e1 = Edge(3, 4, 6)
		assert(e1.X is 3)
		assert(e1.Y is 4)
		assert(e1.player is 6)

	def testEdgePrint(self):
		"""
		Method: testEdgePrint
		--------------------------
		Tests to make sure the stringification of Edge
		is correct.  Tests for Edge with/without roads.
		--------------------------
		"""
		print "Running testEdgePrint...."

		# Test with Edge at (1,2) with road ultimately built
		# by Player 5
		e1 = Edge(1, 2)
		assert(e1.__repr__() == "Unoccupied (1, 2)")

		e1.build(5)
		assert(e1.__repr__() == "R5 (1, 2)")

		# Test with Edge at (5, 6) with road ultimately built
		# by Player 2
		e1 = Edge(5, 6)
		assert(e1.__repr__() == "Unoccupied (5, 6)")

		e1.build(2)
		assert(e1.__repr__() == "R2 (5, 6)")

	def testEdgeIsOccupied(self):
		"""
		Method: testEdgeIsOccupied
		--------------------------
		Tests to make sure an Edge correctly reports whether or
		not it is occupied.
		--------------------------
		"""
		print "Running testEdgeIsOccupied...."

		# Test with Edge at (3,4) and road built by Player 2
		e1 = Edge(3, 4)
		assert(not e1.isOccupied()) # Not occupied initially

		# Build a road (now occupied)
		e1.build(2)
		assert(e1.isOccupied())

		# Test with Edge at (1, 2) and road built by player 5
		e1 = Edge(1, 2)
		assert(not e1.isOccupied()) # Not occupied initially

		# Build a road (now occupied)
		e1.build(5)
		assert(e1.isOccupied())

	def testEdgeCopy(self):
		"""
		Method: testEdgeCopy
		--------------------------
		Tests to make sure the deepCopy method on Edge
		properly deep copies a given edge.
		--------------------------
		"""
		print "Running testEdgeCopy....."

		e1 = Edge(1, 2, 4)
		e2 = e1.deepCopy()

		# Make sure they're not the same object
		assert(e1 != e2)

		# Make sure X is not changed
		e1.X = 0
		assert(e2.X != 0)

		# Make sure Y is not changed
		e1.Y = 3
		assert(e2.Y != 3)

		# Make sure the player is not changed
		e1.player = 5
		assert(e2.player != 5)

	def testEdgeBuild(self):
		"""
		Method: testEdgeBuild
		--------------------------
		Tests to make sure building a road on an edge
		updates state properly.  Also makes sure improperly
		building a road raises an exception.
		--------------------------
		"""
		print "Running testEdgeBuild...."

		# Test valid building
		e1 = Edge(1, 2)
		e1.build(3)
		assert(e1.X is 1)
		assert(e1.Y is 2)
		assert(e1.player is 3)

		# Test having the same player build twice on this
		# Edge (should raise an exception but be caught)
		try:
			e1.build(3)
			print "Error: allowed multiple builds by the same player"
		except:
			# Make sure nothing about the Vertex changed
			assert(e1.player is 3)
			assert(e1.X is 1)
			assert(e1.Y is 2)

		# Test having different players both build on this
		# Edge (should raise an exception but be caught)
		try:
			e1.build(4)
			print "Error: allowed multiple builds by different players"
		except:
			# Make sure nothing about the Vertex changed
			assert(e1.player is 3)
			assert(e1.X is 1)
			assert(e1.Y is 2)


	def runAllTests(self):
		"""
		Method: runTests
		--------------------------
		Run all tests for this test class.
		--------------------------
		"""
		print "Running Edge tests...."
		print "----------------------"
		
		self.testEdgeInit()
		print "Success!"
		self.testEdgeCopy()
		print "Success!"
		self.testEdgeBuild()
		print "Success!"
		self.testEdgeIsOccupied()
		print "Success!"
		self.testEdgePrint()
		print "Success!"

