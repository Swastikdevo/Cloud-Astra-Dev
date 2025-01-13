```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        const response = await fetch('https://api.example.com/customers');
        const data = await response.json();
        setCustomers(data);
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    const handleDelete = async (id) => {
        await fetch(`https://api.example.com/customers/${id}`, { method: 'DELETE' });
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <input 
                type="text" 
                placeholder="Search customers..." 
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email}
                        <button onClick={() => handleDelete(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```