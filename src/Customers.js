```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [filteredCustomers, setFilteredCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => setCustomers(data));
    }, []);

    useEffect(() => {
        setFilteredCustomers(
            customers.filter(customer => 
                customer.name.toLowerCase().includes(searchTerm.toLowerCase())
            )
        );
    }, [searchTerm, customers]);

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    return (
        <div>
            <input 
                type="text" 
                placeholder="Search Customers" 
                value={searchTerm} 
                onChange={handleSearchChange} 
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```