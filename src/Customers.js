```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [sortOrder, setSortOrder] = useState("asc");

    useEffect(() => {
        // Fetch initial customer data
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const handleSearch = (e) => {
        setSearchTerm(e.target.value);
    };

    const handleSort = () => {
        const sortedCustomers = [...customers].sort((a, b) => {
            return sortOrder === "asc" ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name);
        });
        setCustomers(sortedCustomers);
        setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input type="text" placeholder="Search Customers" value={searchTerm} onChange={handleSearch} />
            <button onClick={handleSort}>Sort by Name {sortOrder === "asc" ? "↑" : "↓"}</button>
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```