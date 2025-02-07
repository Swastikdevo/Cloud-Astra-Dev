```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        // Simulating fetch from server
        const fetchCustomers = async () => {
            const data = await new Promise(resolve => {
                setTimeout(() => resolve([
                    { id: 1, name: 'Alice', email: 'alice@example.com' },
                    { id: 2, name: 'Bob', email: 'bob@example.com' },
                ]), 1000);
            });
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const handleAddCustomer = () => {
        setCustomers([...customers, { ...newCustomer, id: Date.now() }]);
        setNewCustomer({ name: '', email: '' });
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input 
                type="text" 
                placeholder="Search Customers" 
                value={searchTerm} 
                onChange={(e) => setSearchTerm(e.target.value)} 
            />
            <h2>Add Customer</h2>
            <input 
                type="text" 
                placeholder="Name" 
                value={newCustomer.name} 
                onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })} 
            />
            <input 
                type="email" 
                placeholder="Email" 
                value={newCustomer.email} 
                onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })} 
            />
            <button onClick={handleAddCustomer}>Add</button>
            <h2>Customer List</h2>
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```