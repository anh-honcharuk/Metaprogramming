open class Some {
    private val f: (     Int ) -> Int = { a: Int -> a * 2 }
    fun foo(): Int {        val test: Int = 12
        for (i in 10..42) {            println(when {                i < test -> -1
                i > test -> 1
                else -> 0
            })
        }
}

class AnotherClass<T : Any> : Some()