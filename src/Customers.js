```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '', phone: '' });
    
    useEffect(() => {
        // Fetch initial customer data
        const fetchData = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchData();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewCustomer({ ...newCustomer, [name]: value });
    };

    const addCustomer = async () => {
        await fetch('/api/customers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newCustomer)
        });
        setCustomers([...customers, newCustomer]);
        setNewCustomer({ name: '', email: '', phone: '' });
    };

    const handleDelete = async (id) => {
        await fetch(`/api/customers/${id}`, {
            method: 'DELETE'
        });
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    return (
        <div>
            <h2>Customer Management</h2>
            <input name="name" value={newCustomer.name} onChange={handleInputChange} placeholder="Name" />
            <input name="email" value={newCustomer.email} onChange={handleInputChange} placeholder="Email" />
            <input name="phone" value={newCustomer.phone} onChange={handleInputChange} placeholder="Phone" />
            <button onClick={addCustomer}>Add Customer</button>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email} - {customer.phone}
                        <button onClick={() => handleDelete(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```