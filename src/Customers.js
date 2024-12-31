```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        // Fetch customer data from an API (pseudo)
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewCustomer({ ...newCustomer, [name]: value });
    };

    const addCustomer = () => {
        setCustomers([...customers, newCustomer]);
        setNewCustomer({ name: '', email: '' });
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <input type="text" name="name" placeholder="Name" value={newCustomer.name} onChange={handleInputChange} />
            <input type="email" name="email" placeholder="Email" value={newCustomer.email} onChange={handleInputChange} />
            <button onClick={addCustomer}>Add Customer</button>
            <ul>
                {customers.map((customer, index) => (
                    <li key={index}>
                        {customer.name} - {customer.email}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```