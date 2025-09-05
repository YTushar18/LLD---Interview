

✅ SOLID Principles Used

Principle	Applied In	Explanation
S: Single Responsibility Principle	File, Folder, StorageService	Each class has one clear responsibility: File holds data, Folder organizes contents, StorageService handles operations like upload/download/delete.
O: Open/Closed Principle	FileEntity base class and polymorphic File, Folder	New file types (e.g., Symlink, CompressedFile) can be added without modifying core logic.
L: Liskov Substitution Principle	FileEntity abstraction	File and Folder can be used interchangeably where FileEntity is expected.
I: Interface Segregation Principle	Implicitly respected by defining minimal, purposeful interfaces (e.g., add, remove only exist on Folder).	
D: Dependency Inversion Principle	(Future phase: adapter pattern for backends like S3)	High-level modules (e.g., StorageService) will depend on abstract StorageBackend interface instead of concrete implementation.


⸻

🎯 Design Patterns Used

Pattern	Applied In	Description
Composite Pattern	FileEntity, File, Folder	Enables treating individual files and folders (which contain files) uniformly.
Strategy-Ready Design	StorageService	Methods like upload, delete, and download are encapsulated, so backends or access policies can be swapped later.
Factory-Ready	Not yet, but folder/file creation could be abstracted into a factory for extended types.	
Command Pattern (Optional Extension)	Could be used to log or undo actions (e.g., upload/delete).	
Adapter Pattern (For next phase)	Could abstract StorageBackend (e.g., LocalStorage vs. S3) to be plug-n-play.	


⸻

🧱 Key Components Summary

Component	Responsibility
FileEntity (Abstract)	Base class for any storable entity (File, Folder)
File	Leaf node; holds actual content
Folder	Composite node; can hold File and Folder children
StorageService	Operates on a folder tree to perform file operations (upload/download/delete)
main() function	Simulates usage; creates structure, uploads files, shows results


⸻

💡 Clean Code Notes
	•	Encapsulation: File content, folder contents, and path resolution are hidden behind clear APIs.
	•	Extensibility: Easy to add features like encryption, logging, cloud backends, or versioning.
	•	Testability: Logic is modular and can be tested independently.
