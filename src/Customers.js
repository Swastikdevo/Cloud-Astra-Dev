```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const handleDelete = async (id) => {
        await fetch(`/api/customers/${id}`, { method: 'DELETE' });
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <input
                type="text"
                placeholder="Search customers..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} <button onClick={() => handleDelete(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```