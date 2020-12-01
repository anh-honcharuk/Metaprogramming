package search


fun <T: Comparable<T>> binarySearch(array: Array<T>, key: T): Int {
    return binarySearchHelper(array, key, 0, array.size - 1)
}


fun <T: Comparable<T>> binarySearchHelper(array: Array<T>, key: T, start: Int, end: Int): Int {
    if (start > end) {
        return -1
    }

    val mid = start + (end - start) / 2

    return when {
        array[mid].compareTo(key) == 0 -> mid
        array[mid].compareTo(key) > 0 -> binarySearchHelper(array, key, start, mid - 1)
        else -> binarySearchHelper(array, key, mid + 1, end)
    }
}
