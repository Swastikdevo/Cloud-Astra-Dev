```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagementSystem = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
    const [filter, setFilter] = useState('');

    useEffect(() => {
        // Simulate fetching customers from an API
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const addCustomer = () => {
        setCustomers([...customers, { ...newCustomer, id: Date.now() }]);
        setNewCustomer({ name: '', email: '' });
    };

    const filteredCustomers = customers.filter(customer => customer.name.includes(filter));

    return (
        <div>
            <h1>Customer Management</h1>
            <input 
                type="text" 
                placeholder="Search Customers" 
                value={filter} 
                onChange={e => setFilter(e.target.value)} 
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
            <input 
                type="text" 
                placeholder="Name" 
                value={newCustomer.name} 
                onChange={e => setNewCustomer({ ...newCustomer, name: e.target.value })} 
            />
            <input 
                type="email" 
                placeholder="Email" 
                value={newCustomer.email} 
                onChange={e => setNewCustomer({ ...newCustomer, email: e.target.value })} 
            />
            <button onClick={addCustomer}>Add Customer</button>
        </div>
    );
};
export default CustomerManagementSystem;
```