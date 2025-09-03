# ------------------------------------------------------------
# LRU Cache Design using:
# ✅ HashMap for O(1) lookups
# ✅ Doubly Linked List for O(1) insert/delete operations
# ✅ Command pattern is not used here (not required)
# ✅ Adheres to SOLID Principles
# ------------------------------------------------------------

# -------------------------------
# 🧱 Node class (used in DLL)
# -------------------------------
# S — Single Responsibility: Represents just a cache entry with links.
class Node:
    def __init__(self, key: int, value: int):
        self.key = key              # Unique identifier
        self.value = value          # Associated value
        self.prev = None            # Pointer to previous node
        self.next = None            # Pointer to next node


# -------------------------------
# 🚀 LRU Cache Class
# -------------------------------
# S — Editor class has 1 responsibility: manage the cache.
# O — New eviction policy can be added by subclassing.
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # HashMap: key -> Node

        # Dummy head and tail nodes to avoid null checks
        # These act as sentinels in the doubly linked list
        self.head = Node(0, 0)
        self.tail = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

    # -----------------------------------------
    # Helper Method: Add node right after head
    # Used when adding a new node or moving one to front
    # -----------------------------------------
    def _add_node(self, node):
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    # -----------------------------------------
    # Helper Method: Remove node from DLL
    # Used during eviction or movement
    # -----------------------------------------
    def _remove_node(self, node):
        prev = node.prev
        next = node.next

        prev.next = next
        next.prev = prev

    # -----------------------------------------
    # Helper Method: Move node to front (MRU)
    # Called during access (get or put)
    # -----------------------------------------
    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_node(node)

    # -----------------------------------------
    # Helper Method: Pop the last node (LRU)
    # Called when cache exceeds capacity
    # -----------------------------------------
    def _pop_tail(self):
        lru = self.tail.prev
        self._remove_node(lru)
        return lru

    # -----------------------------------------
    # 📥 GET Operation: O(1)
    # 1. Fetch node from map
    # 2. Move it to head (MRU)
    # -----------------------------------------
    def get(self, key: int) -> int:
        node = self.cache.get(key)

        if not node:
            return -1  # Not found

        self._move_to_head(node)
        return node.value

    # -----------------------------------------
    # 📝 PUT Operation: O(1)
    # 1. If key exists, update value + move to head
    # 2. If not, insert new node
    # 3. If over capacity, evict LRU from tail
    # -----------------------------------------
    def put(self, key: int, value: int) -> None:
        node = self.cache.get(key)

        if node:
            # Update value & move to front
            node.value = value
            self._move_to_head(node)
        else:
            # Create new node and add to list and map
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)

            # Check for overflow and evict LRU
            if len(self.cache) > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]

if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))  # returns 1
    cache.put(3, 3)       # evicts key 2
    print(cache.get(2))  # returns -1
    cache.put(4, 4)       # evicts key 1
    print(cache.get(1))  # returns -1
    print(cache.get(3))  # returns 3
    print(cache.get(4))  # returns 4