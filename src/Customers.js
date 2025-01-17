```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
  
    useEffect(() => {
        fetchCustomers();
    }, []);
  
    const fetchCustomers = async () => {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
    };
  
    const addCustomer = async () => {
        const response = await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email })
        });
        if (response.ok) {
            fetchCustomers();
            setName('');
            setEmail('');
        }
    };
  
    const deleteCustomer = async (id) => {
        await fetch(`/api/customers/${id}`, { method: 'DELETE' });
        fetchCustomers();
    };
  
    return (
        <div>
            <h1>Customer Management</h1>
            <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Customer Name"
            />
            <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Customer Email"
            />
            <button onClick={addCustomer}>Add Customer</button>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email} 
                        <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```