```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [editingCustomer, setEditingCustomer] = useState(null);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
    };

    const handleSearch = (e) => {
        setSearchTerm(e.target.value);
    };

    const handleEdit = (customer) => {
        setEditingCustomer(customer);
        setNewCustomer(customer);
    };

    const handleChange = (e) => {
        setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });
    };

    const handleSave = async () => {
        const response = await fetch(`/api/customers/${newCustomer.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        if (response.ok) {
            fetchCustomers();
            setEditingCustomer(null);
            setNewCustomer({ name: '', email: '' });
        }
    };

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <input type="text" value={searchTerm} onChange={handleSearch} placeholder="Search Customers" />
            {editingCustomer ? (
                <div>
                    <input name="name" value={newCustomer.name} onChange={handleChange} />
                    <input name="email" value={newCustomer.email} onChange={handleChange} />
                    <button onClick={handleSave}>Save</button>
                </div>
            ) : (
                <div>
                    {filteredCustomers.map(customer => (
                        <div key={customer.id}>
                            <span>{customer.name}</span>
                            <span>{customer.email}</span>
                            <button onClick={() => handleEdit(customer)}>Edit</button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default CustomerManagement;
```