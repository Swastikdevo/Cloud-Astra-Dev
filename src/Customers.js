```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [filteredCustomers, setFilteredCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => {
                setCustomers(data);
                setFilteredCustomers(data);
            });
    }, []);

    useEffect(() => {
        setFilteredCustomers(
            customers.filter(customer => 
                customer.name.toLowerCase().includes(searchTerm.toLowerCase())
            )
        );
    }, [searchTerm, customers]);

    return (
        <div>
            <input 
                type="text" 
                placeholder="Search customers" 
                value={searchTerm} 
                onChange={(e) => setSearchTerm(e.target.value)} 
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