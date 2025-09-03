Awesome! Let’s move on to LLD Problem 2: LRU Cache — one of the most commonly asked system design problems in interviews.

⸻

✅ Problem: LRU Cache (Least Recently Used)

💡 What It Is:

An in-memory cache that:
	•	Stores up to N items (capacity)
	•	When full, removes the Least Recently Used item
	•	Provides O(1) access to:
	•	get(key) → returns value
	•	put(key, value) → insert/update key-value pair

⸻

🧱 Core Requirements

Feature	Requirement
get(key)	Return value if exists, else -1. Mark as most recently used.
put(key, val)	Insert or update key-value. If full, evict LRU item.


⸻

🎯 Design Constraints
	•	All operations must be O(1) time
	•	Use doubly linked list + hashmap

⸻

🧠 High-Level Design

📦 Components
	1.	HashMap → Key → Node (stores key, value)
	2.	Doubly Linked List → Maintains usage order (head = most recent, tail = least recent)

🔁 Operations

Operation	Action
get(key)	Move node to head (most recently used)
put(key, value)	Insert/update node, evict tail if over capacity


⸻

🧩 Class Diagram

LRUCache
 ├── capacity: int
 ├── cache: Dict[key, Node]
 ├── head & tail (Doubly linked list sentinels)

Node
 ├── key, value
 ├── prev, next


⸻

✅ Summary

Concept	Implementation
Access Time	O(1) via hashmap
Order Maintenance	Doubly linked list
Eviction	Remove from tail
Update/Promotion	Move to head


⸻

🧠 SOLID + Design Patterns

Principle	Application
S	Node (just data), LRUCache (logic)
O	Can replace eviction logic if needed
L	Nodes are generic; interchangeable
I	No bloated interfaces
D	Uses abstraction of node links, not concrete structures

