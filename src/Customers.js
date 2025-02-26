```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState('');

    useEffect(() => {
        fetch('/api/customers')
            .then(response => response.json())
            .then(data => setCustomers(data));
    }, []);

    const addCustomer = () => {
        if (newCustomer) {
            const updatedCustomers = [...customers, { name: newCustomer }];
            setCustomers(updatedCustomers);
            setNewCustomer('');
            // Simulating a POST request
            fetch('/api/customers', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: newCustomer })
            });
        }
    };

    const removeCustomer = (name) => {
        const updatedCustomers = customers.filter(customer => customer.name !== name);
        setCustomers(updatedCustomers);
        // Simulating a DELETE request
        fetch(`/api/customers/${name}`, { method: 'DELETE' });
    };

    return (
        <div>
            <h2>Customer Management</h2>
            <input
                type="text"
                value={newCustomer}
                onChange={e => setNewCustomer(e.target.value)}
                placeholder="Add new customer"
            />
            <button onClick={addCustomer}>Add</button>
            <ul>
                {customers.map((customer, index) => (
                    <li key={index}>
                        {customer.name}
                        <button onClick={() => removeCustomer(customer.name)}>Remove</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerList;
```