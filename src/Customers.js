```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredCustomers, setFilteredCustomers] = useState([]);

    useEffect(() => {
        fetchCustomers();
    }, []);

    useEffect(() => {
        setFilteredCustomers(
            customers.filter(customer => 
                customer.name.toLowerCase().includes(searchTerm.toLowerCase())
            )
        );
    }, [searchTerm, customers]);

    const fetchCustomers = async () => {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
    };

    const handleSearchChange = (e) => {
        setSearchTerm(e.target.value);
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Search customers"
                value={searchTerm}
                onChange={handleSearchChange}
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>{customer.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```