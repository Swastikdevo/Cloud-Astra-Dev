```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
    };

    const handleFilterChange = (event) => {
        setFilter(event.target.value);
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input 
                type="text" 
                placeholder="Filter by name" 
                value={filter} 
                onChange={handleFilterChange} 
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email}
                        <button onClick={() => alert(`Editing ${customer.name}`)}>Edit</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```