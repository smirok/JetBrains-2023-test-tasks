import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.core.subcommands
import com.github.ajalt.clikt.parameters.arguments.argument
import com.github.ajalt.clikt.parameters.options.option
import java.io.File

class Main : CliktCommand() {
    override fun run() {

    }
}

class Base : CliktCommand(name = "base") {
    private val firstTree by argument()
    private val secondTree by argument()

    override fun run() {
        val firstTreeRepresentation = File(firstTree).readText()
        val secondTreeRepresentation = File(secondTree).readText()
        println((Tree(firstTreeRepresentation).transformTo(Tree(secondTreeRepresentation))).joinToString())
    }
}

class Bonus : CliktCommand(name = "bonus") {
    private val treePath by option()

    override fun run() {
        val tree = initTree(treePath)
        println(tree)

        while (true) {
            val command = readln()

            if (command.startsWith("SAVE")) {
                save(command, tree)
            } else if (command.startsWith("ADD")) {
                add(command, tree)
            } else if (command.startsWith("REMOVE")) {
                remove(command, tree)
            } else if (command == "EXIT") {
                break
            } else {
                println("Wrong command. Try again.")
                continue
            }
        }
    }

    private fun remove(command: String, tree: Tree) {
        val nodeId = command
            .substring(7 until command.lastIndex)
            .toInt()
        tree.remove(nodeId)
        println(tree)
    }

    private fun add(command: String, tree: Tree) {
        val arguments = command
            .substring(4 until command.lastIndex)
            .split(",")
            .map(String::trim)
            .map(String::toInt)
        tree.add(arguments[0], arguments[1])
        println(tree)
    }

    private fun save(command: String, tree: Tree) {
        val path = command.split(" ").last()
        saveTree(tree, path)
        println("Tree was saved in '$path'")
    }
}

fun main(args: Array<String>) = Main().subcommands(Base(), Bonus()).main(args)
