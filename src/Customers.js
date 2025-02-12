```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = ({ customers, onDelete }) => {
    const [searchTerm, setSearchTerm] = useState('');

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <input
                type="text"
                placeholder="Search Customers"
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>
                        <span>{customer.name}</span>
                        <button onClick={() => onDelete(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => setCustomers(data));
    }, []);

    const handleDelete = id => {
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <CustomerList customers={customers} onDelete={handleDelete} />
        </div>
    );
};

export default CustomerManagement;
```