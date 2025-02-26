```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCustomers = async () => {
            setLoading(true);
            try {
                const response = await axios.get('/api/customers');
                setCustomers(response.data);
            } catch (error) {
                console.error('Error fetching customers', error);
            } finally {
                setLoading(false);
            }
        };
        fetchCustomers();
    }, []);

    const handleChange = (e) => {
        setNewCustomer({
            ...newCustomer,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/customers', newCustomer);
            setCustomers([...customers, response.data]);
            setNewCustomer({ name: '', email: '' });
        } catch (error) {
            console.error('Error adding customer', error);
        }
    };

    return (
        <div>
            <h1>Customer Management</h1>
            {loading ? <p>Loading...</p> : (
                <ul>
                    {customers.map(customer => (
                        <li key={customer.id}>{customer.name} - {customer.email}</li>
                    ))}
                </ul>
            )}
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" value={newCustomer.name} onChange={handleChange} placeholder="Name" required />
                <input type="email" name="email" value={newCustomer.email} onChange={handleChange} placeholder="Email" required />
                <button type="submit">Add Customer</button>
            </form>
        </div>
    );
};

export default CustomerManagement;
```