# getAusweis
Small Python tooling to batch-extract StudentID Information from PDF-Invoices

When selling School-Pictures with portraitbox.com i need to know which Customer bought a StudenID card in order to print only the cards that are actually ordered. Sadly, Portraitbox does not give me this information in machine readable form. The only way to get to this information is to download all the PDF Invoices in one directory. This download can be requested with one click.

This script no looks through all .pdf Invoices in a specified directory and scans them for the keyword "Schülerausweis", indicating that this customer bought a StudentID. It then fetches the Order-Code which was used by the customer to log in to the Shop as well as the order number. The script then creates a .csv file with Order Number and Order-Code. this allows me to join the .csv file with my existing .xlsx files to map the Order-Code to the Name of a student which again can be joined with my print database containing Birthday, Graduation Day, Name and path tho ID-Photo.

All in all this tool allows me to get from a directory with .pdf files to a directly printable table that contains all neccessary information for the print of the StudentID for everyone that bought one.

In particular the script also handels orders with multiple codes and multiple StudentID orders for diffrent Students (e.g. orders for siblings). In this case the script creates a seperate entry with the same Invoice number but different Order-Code.

Optionally a third column with all Classes for which Photos were ordered can be included in the .csv file for extra convenience and supervision.
