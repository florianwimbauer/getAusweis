# getAusweis
Small Python tooling to batch-extract StudentID Information from PDF-Invoices and bring them into a printable format through merging with other tables

When selling School-Pictures with [Portraitbox.com](https://portraitbox.com) i need to know which customer bought a StudenID card in order to print only the cards that are actually ordered. Sadly, Portraitbox does not provie this data in machine readable form. The only way to get to this information is to download all the PDF Invoices in one directory. This download can be requested within the admin interface.

The point of this skript is to look through all ```.pdf``` Invoices in a specified directory and scan them for the keyword _Schülerausweis_, indicating that this customer bought a StudentID. It then fetches the Order-Code which was used by the customer to log in to the Shop as well as the order number. The script then creates a ```.csv``` file with Order Number and Order-Code. 
The Order-Code allows me to match the StudentID-Order to the Name of a specific student through joining it with my existing data that was used to set up the store at the beginning. This can again be joined with my print database containing birthday, graduation day, name and path tho ID-Photo which can be directly fed to the Card-Printer.

Since the ```.pdf``` files are sorted by Order Number, the ```.csv``` file is also sorted by Ordernumber. By keeping up this order all the way until printing, it also alows for easy packaging since the StudentIDs are in the same order as the orders themselves.

In summary, this tool allows me to get from a directory with 4 digit amount of ```.pdf``` files to a directly printable table that contains all neccessary information to start one printjob of StudentIDs for everyone that bought one.

In particular the script also handels orders with multiple codes / multiple StudentID orders for diffrent Students (e.g. orders for siblings). In this case the script creates a seperate entry with the same Invoice number but different Order-Code.

Optionally a third column with all Classes for which Photos were ordered in a specific order can be included in the ```.csv``` file for extra convenience and supervision.
