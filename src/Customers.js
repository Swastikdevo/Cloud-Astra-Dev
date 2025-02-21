```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => setCustomers(data));
    }, []);

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div>
            <input
                type="text"
                placeholder="Search Customers"
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```