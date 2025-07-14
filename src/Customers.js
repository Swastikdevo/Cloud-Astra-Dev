```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onSubmit }) => {
    const [customer, setCustomer] = useState({ name: '', email: '', phone: '' });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCustomer({ ...customer, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(customer);
        setCustomer({ name: '', email: '', phone: '' });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input name="name" value={customer.name} onChange={handleChange} placeholder="Name" required />
            <input name="email" value={customer.email} onChange={handleChange} placeholder="Email" required type="email" />
            <input name="phone" value={customer.phone} onChange={handleChange} placeholder="Phone" />
            <button type="submit">Add Customer</button>
        </form>
    );
};

const CustomerList = ({ customers, onDelete }) => {
    return (
        <ul>
            {customers.map((customer, index) => (
                <li key={index}>
                    {customer.name} - {customer.email} - {customer.phone}
                    <button onClick={() => onDelete(index)}>Delete</button>
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

    const deleteCustomer = (index) => {
        setCustomers(customers.filter((_, i) => i !== index));
    };

    return (
        <div>
            <h2>Customer Management System</h2>
            <CustomerForm onSubmit={addCustomer} />
            <CustomerList customers={customers} onDelete={deleteCustomer} />
        </div>
    );
};

export default CustomerManagement;
```