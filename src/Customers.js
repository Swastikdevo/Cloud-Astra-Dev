```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
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

    const handleAddCustomer = async (e) => {
        e.preventDefault();
        await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        setCustomers([...customers, newCustomer]);
        setNewCustomer({ name: '', email: '' });
    };

    const handleSearch = (e) => {
        setSearchTerm(e.target.value);
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
                onChange={handleSearch} 
            />
            <form onSubmit={handleAddCustomer}>
                <input 
                    type="text" 
                    name="name" 
                    placeholder="Name" 
                    value={newCustomer.name} 
                    onChange={handleInputChange} 
                    required 
                />
                <input 
                    type="email" 
                    name="email" 
                    placeholder="Email" 
                    value={newCustomer.email} 
                    onChange={handleInputChange} 
                    required 
                />
                <button type="submit">Add Customer</button>
            </form>
            <ul>
                {filteredCustomers.map((customer, index) => (
                    <li key={index}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```