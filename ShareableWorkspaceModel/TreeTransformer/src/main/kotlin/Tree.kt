import kotlinx.serialization.Serializable
import kotlin.properties.Delegates

const val DEFAULT_ROOT = 1

@Serializable
class Tree(private val treeRepresentation: String) {
    private val parentToChildren: MutableMap<Int, MutableSet<Int>> = mutableMapOf()
    private var root: Int by Delegates.notNull()

    constructor() : this("")

    init {
        if (treeRepresentation.isEmpty()) {
            root = DEFAULT_ROOT
        } else {
            innerInit()
        }
    }

    private fun innerInit() {
        val edgeList = treeRepresentation
            .subSequence(1 until treeRepresentation.lastIndex - 1)
            .split("][")
            .map { edge ->
                val nodeIds = edge.split(",").map(String::trim).map(String::toInt)
                Pair(nodeIds[0], nodeIds[1])
            }
        edgeList.forEach { (parent, child) ->
            add(parent, child)
        }
        val (parents, children) = edgeList.unzip()
        root = parents.minus(children.toSet()).first()
    }

    fun transformTo(tree: Tree): List<String> {
        if (root != tree.root) {
            error("Cannot transform with root changing")
        }

        return recursiveTransformTo(root, tree)
    }

    fun add(parent: Int, child: Int) {
        if (!parentToChildren.containsKey(parent)) {
            parentToChildren[parent] = hashSetOf()
        }
        parentToChildren[parent]?.add(child)
    }

    fun remove(nodeId: Int) {
        if (nodeId == root) {
            println("Root can't be removed!")
            return
        }

        val children = parentToChildren[nodeId] ?: emptySet()

        if (children.isNotEmpty()) {
            println("Non-leaf node can't be removed!")
            return
        }

        for (parent in parentToChildren.keys) {
            parentToChildren[parent]?.remove(nodeId)
        }
    }

    override fun toString(): String {
        val nodeRepresentations = mutableListOf("L__$root")
        val leftMargin = nodeRepresentations[0].length
        for (child in parentToChildren[root] ?: emptySet()) {
            nodeRepresentations.add(recursiveToString(leftMargin, child))
        }
        return nodeRepresentations.joinToString("\n")
    }

    private fun recursiveToString(leftMargin: Int, node: Int): String {
        val nodeRepresentations = mutableListOf(" ".repeat(leftMargin) + "L__$node")
        val increasedLeftMargin = nodeRepresentations[0].length
        for (child in parentToChildren[node] ?: emptySet()) {
            nodeRepresentations.add(recursiveToString(increasedLeftMargin, child))
        }
        return nodeRepresentations.joinToString("\n")
    }

    private fun recursiveTransformTo(currentNode: Int, tree: Tree): List<String> {
        val children = parentToChildren[currentNode] ?: emptySet()
        val anotherChildren = tree.parentToChildren[currentNode] ?: emptySet()

        val nodesToRemove = children.minus(anotherChildren)
        val nodesToAdd = anotherChildren.minus(children)
        val commonNodes = children.intersect(anotherChildren)

        val result: ArrayList<String> = arrayListOf()
        nodesToRemove.forEach { node -> result.addAll(removeSubtree(node)) }
        nodesToAdd.forEach { node -> result.addAll(addSubtree(node, currentNode, tree)) }
        commonNodes.forEach { node -> result.addAll(recursiveTransformTo(node, tree)) }
        return result
    }

    private fun addSubtree(node: Int, parent: Int, tree: Tree): List<String> {
        add(parent, node)
        val children = tree.parentToChildren[node] ?: emptyList()
        val result = children.map { addSubtree(it, node, tree) }.flatten()

        return result + listOf("ADD($parent,$node)")
    }

    private fun removeSubtree(node: Int): List<String> {
        val children = parentToChildren[node] ?: emptyList()
        val result = children.map { removeSubtree(it) }.flatten()
        remove(node)

        return result + listOf("REMOVE($node)")
    }
}
