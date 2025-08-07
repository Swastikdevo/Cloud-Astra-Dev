```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState('');
    const [searchTerm, setSearchTerm] = useState('');

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
            setCustomers([...customers, { name: newCustomer }]);
            setNewCustomer('');
        }
    };

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input
                type="text"
                placeholder="Search Customer"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <ul>
                {filteredCustomers.map((customer, index) => (
                    <li key={index}>{customer.name}</li>
                ))}
            </ul>
            <input
                type="text"
                placeholder="New Customer Name"
                value={newCustomer}
                onChange={(e) => setNewCustomer(e.target.value)}
            />
            <button onClick={addCustomer}>Add Customer</button>
        </div>
    );
};

export default CustomerManagement;
```