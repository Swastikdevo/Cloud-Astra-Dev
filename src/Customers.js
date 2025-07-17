```javascript
import React, { useState } from 'react';

const CustomerForm = ({ onAddCustomer }) => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [address, setAddress] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onAddCustomer({ name, email, address });
        setName('');
        setEmail('');
        setAddress('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text" 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                placeholder="Customer Name" 
                required 
            />
            <input 
                type="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                placeholder="Email Address" 
                required 
            />
            <input 
                type="text" 
                value={address} 
                onChange={(e) => setAddress(e.target.value)} 
                placeholder="Address" 
                required 
            />
            <button type="submit">Add Customer</button>
        </form>
    );
};

const CustomerList = ({ customers }) => {
    return (
        <ul>
            {customers.map((customer, index) => (
                <li key={index}>
                    {customer.name} - {customer.email}
                </li>
            ))}
        </ul>
    );
};

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);

    const addCustomer = (customer) => {
        setCustomers([...customers, customer]);
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <CustomerForm onAddCustomer={addCustomer} />
            <CustomerList customers={customers} />
        </div>
    );
};

export default CustomerManagement;
```