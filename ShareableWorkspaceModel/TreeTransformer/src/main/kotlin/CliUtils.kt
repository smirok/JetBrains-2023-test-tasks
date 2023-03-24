import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import java.io.File

internal fun saveTree(tree: Tree, path: String) {
    val encodedTree = Json.encodeToString(Tree.serializer(), tree)
    File(path).writeText(encodedTree)
}

internal fun initTree(treePath: String?): Tree = treePath?.let {
    Json.decodeFromString(File(it).readText())
} ?: Tree()

