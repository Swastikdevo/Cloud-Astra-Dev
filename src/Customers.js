```javascript
import React, { useState } from 'react';

const CustomerForm = ({ onSubmit }) => {
    const [customer, setCustomer] = useState({ name: '', email: '', phone: '' });

    const handleChange = (e) => {
        setCustomer({ ...customer, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(customer);
        setCustomer({ name: '', email: '', phone: '' });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="name" placeholder="Name" value={customer.name} onChange={handleChange} required />
            <input type="email" name="email" placeholder="Email" value={customer.email} onChange={handleChange} required />
            <input type="tel" name="phone" placeholder="Phone" value={customer.phone} onChange={handleChange} required />
            <button type="submit">Add Customer</button>
        </form>
    );
};

const CustomerList = ({ customers }) => (
    <ul>
        {customers.map((customer, index) => (
            <li key={index}>{customer.name} - {customer.email} - {customer.phone}</li>
        ))}
    </ul>
);

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);

    const addCustomer = (customer) => {
        setCustomers([...customers, customer]);
    };

    return (
        <div>
            <h1>Customer Management System</h1>
            <CustomerForm onSubmit={addCustomer} />
            <CustomerList customers={customers} />
        </div>
    );
};

export default CustomerManagement;
```