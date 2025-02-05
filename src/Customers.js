```javascript
import React, { useState, useEffect } from 'react';

const CustomerTable = ({ customers }) => {
    const [sortedCustomers, setSortedCustomers] = useState([]);

    useEffect(() => {
        setSortedCustomers(customers.sort((a, b) => a.name.localeCompare(b.name)));
    }, [customers]);

    return (
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {sortedCustomers.map(customer => (
                    <tr key={customer.id}>
                        <td>{customer.name}</td>
                        <td>{customer.email}</td>
                        <td>{customer.isActive ? 'Active' : 'Inactive'}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '', isActive: true });

    const addCustomer = () => {
        setCustomers([...customers, { ...newCustomer, id: Date.now() }]);
        setNewCustomer({ name: '', email: '', isActive: true });
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <input 
                type="text" 
                placeholder="Name" 
                value={newCustomer.name} 
                onChange={(e) => setNewCustomer({...newCustomer, name: e.target.value})} 
            />
            <input 
                type="email" 
                placeholder="Email" 
                value={newCustomer.email} 
                onChange={(e) => setNewCustomer({...newCustomer, email: e.target.value})} 
            />
            <button onClick={addCustomer}>Add Customer</button>
            <CustomerTable customers={customers} />
        </div>
    );
};

export default CustomerManagement;
```