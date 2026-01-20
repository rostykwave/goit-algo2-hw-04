from typing import List


class TrieNode(dict):
    """Simple Trie node implemented as a dict for children with an "_end" marker."""


class Trie:
    """A minimal prefix-trie implementation.

    - Supports insertion and membership checks.
    - Stores words added via `insert` and allows collecting all stored words.
    """

    def __init__(self) -> None:
        self._root: TrieNode = TrieNode()
        self._suffix_root: TrieNode = TrieNode()
        self._word_count = 0
        self._END = "_end"

    def insert(self, word: str) -> None:
        """Insert `word` into the trie. Raises TypeError for non-str input."""
        if not isinstance(word, str):
            raise TypeError("word must be a str")
        node = self._root
        for ch in word:
            if ch not in node:
                node[ch] = TrieNode()
            node = node[ch]
        node[self._END] = True

        rev_word = word[::-1]
        node = self._suffix_root
        for ch in rev_word:
            if ch not in node:
                node[ch] = TrieNode()
            node = node[ch]
        node[self._END] = True

        self._word_count += 1

    def put(self, word: str, value=None) -> None:
        """Alias for insert, ignoring value."""
        self.insert(word)

    def contains(self, word: str) -> bool:
        """Return True if `word` is present exactly in the trie."""
        if not isinstance(word, str):
            raise TypeError("word must be a str")
        node = self._root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return bool(node.get(self._END, False))

    def _node_for_prefix(self, prefix: str, root=None):
        """Return the node corresponding to the end of `prefix`, or None."""
        if root is None:
            root = self._root
        node = root
        for ch in prefix:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def starts_with(self, prefix: str) -> bool:
        """Return True if the trie contains the path for `prefix` (may not be a complete word).

        Note: this method only checks whether the prefix path exists; it does NOT
        guarantee there is a stored word that has the prefix (use Homework.has_prefix
        for that semantic).
        """
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a str")
        return self._node_for_prefix(prefix) is not None

    def _count_words_in_subtree(self, node):
        """Count the number of complete words in the subtree rooted at node."""
        if node is None:
            return 0
        count = 0
        stack = [node]
        while stack:
            cur = stack.pop()
            if cur.get(self._END):
                count += 1
            for k, child in cur.items():
                if k != self._END:
                    stack.append(child)
        return count

    def words(self) -> List[str]:
        """Return a list of all stored words (insertion order not guaranteed)."""
        out: List[str] = []
        self._collect_from_node(self._root, "", out)
        return out


class Homework(Trie):
    """Homework extension of Trie with two additional required methods."""

    def count_words_with_suffix(self, pattern: str) -> int:
        """Count stored words that end with `pattern`.

        - `pattern` must be a str, otherwise raises TypeError.
        - An empty `pattern` matches all stored words (by convention).
        - Returns an int (0 or positive).
        """
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a str")
        if pattern == "":
            return self._word_count
        rev_pattern = pattern[::-1]
        node = self._node_for_prefix(rev_pattern, self._suffix_root)
        return self._count_words_in_subtree(node)

    def has_prefix(self, prefix: str) -> bool:
        """Return True iff there exists at least one stored word that starts with `prefix`.

        - `prefix` must be a str, otherwise raises TypeError.
        - An empty `prefix` returns True iff the trie contains at least one word.
        """
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a str")
        node = self._node_for_prefix(prefix)
        if node is None:
            return False
        
        stack = [node]
        while stack:
            cur = stack.pop()
            if cur.get(self._END):
                return True
            for k, child in cur.items():
                if k == self._END:
                    continue
                stack.append(child)
        return False
