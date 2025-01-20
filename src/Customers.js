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
            setCustomers([...customers, { id: Date.now(), name: newCustomer }]);
            setNewCustomer('');
        }
    };

    const deleteCustomer = (id) => {
        setCustomers(customers.filter(customer => customer.id !== id));
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
            <button onClick={addCustomer}>Add Customer</button>
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