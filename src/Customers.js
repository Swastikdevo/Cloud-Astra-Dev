```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [customer, setCustomer] = useState({ name: '', age: '', email: '' });
    const [filter, setFilter] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchData();
    }, []);

    const handleChange = (e) => {
        setCustomer({ ...customer, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(customer),
        });
        const newCustomer = await response.json();
        setCustomers([...customers, newCustomer]);
        setCustomer({ name: '', age: '', email: '' });
    };

    const filteredCustomers = customers.filter((c) => 
        c.name.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div>
            <h1>Customer Management</h1>
            <input
                type="text"
                placeholder="Search Customers"
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
            />
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="name"
                    placeholder="Name"
                    value={customer.name}
                    onChange={handleChange}
                    required
                />
                <input
                    type="number"
                    name="age"
                    placeholder="Age"
                    value={customer.age}
                    onChange={handleChange}
                    required
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={customer.email}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Add Customer</button>
            </form>
            <ul>
                {filteredCustomers.map((cust) => (
                    <li key={cust.id}>{`${cust.name} - ${cust.age} - ${cust.email}`}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```