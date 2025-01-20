```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [editingId, setEditingId] = useState(null);

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
        };
        fetchCustomers();
    }, []);

    const handleAddOrUpdate = async () => {
        if (editingId) {
            await fetch(`/api/customers/${editingId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email }),
            });
        } else {
            await fetch('/api/customers', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email }),
            });
        }
        setName('');
        setEmail('');
        setEditingId(null);
        fetchCustomers();
    };

    const handleEdit = (customer) => {
        setName(customer.name);
        setEmail(customer.email);
        setEditingId(customer.id);
    };

    const handleDelete = async (id) => {
        await fetch(`/api/customers/${id}`, {
            method: 'DELETE',
        });
        fetchCustomers();
    };

    return (
        <div>
            <h2>Customer Management</h2>
            <input 
                type="text" 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                placeholder="Customer Name" 
            />
            <input 
                type="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                placeholder="Customer Email" 
            />
            <button onClick={handleAddOrUpdate}>
                {editingId ? 'Update Customer' : 'Add Customer'}
            </button>
            <ul>
                {customers.map((customer) => (
                    <li key={customer.id}>
                        {customer.name} ({customer.email})
                        <button onClick={() => handleEdit(customer)}>Edit</button>
                        <button onClick={() => handleDelete(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```