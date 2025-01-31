```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState('');

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const addCustomer = () => {
        if (newCustomer) {
            const updatedCustomers = [...customers, { name: newCustomer, id: Date.now() }];
            setCustomers(updatedCustomers);
            setNewCustomer('');
        }
    };

    const deleteCustomer = (id) => {
        const updatedCustomers = customers.filter(customer => customer.id !== id);
        setCustomers(updatedCustomers);
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <input 
                type="text" 
                value={newCustomer} 
                onChange={(e) => setNewCustomer(e.target.value)} 
                placeholder="Add new customer"
            />
            <button onClick={addCustomer}>Add</button>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} 
                        <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```