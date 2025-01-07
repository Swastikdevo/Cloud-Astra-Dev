```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCustomer, setSelectedCustomer] = useState(null);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        // Mock fetch customers
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const handleAddCustomer = () => {
        setCustomers([...customers, { ...newCustomer, id: Date.now() }]);
        setNewCustomer({ name: '', email: '' });
    };

    const handleSelectCustomer = (customer) => {
        setSelectedCustomer(customer);
    };

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input
                type="text"
                placeholder="Search customers"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id} onClick={() => handleSelectCustomer(customer)}>
                        {customer.name} - {customer.email}
                    </li>
                ))}
            </ul>
            <h2>Add New Customer</h2>
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
            <button onClick={handleAddCustomer}>Add Customer</button>
            {selectedCustomer && (
                <div>
                    <h3>Selected Customer</h3>
                    <p>Name: {selectedCustomer.name}</p>
                    <p>Email: {selectedCustomer.email}</p>
                </div>
            )}
        </div>
    );
};

export default CustomerManagement;
```