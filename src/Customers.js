```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
    const [editingCustomer, setEditingCustomer] = useState(null);

    useEffect(() => {
        // Mock fetch call
        const fetchCustomers = async () => {
            const data = await fetch('/api/customers');
            const customers = await data.json();
            setCustomers(customers);
        };

        fetchCustomers();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewCustomer({ ...newCustomer, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (editingCustomer) {
            setCustomers(customers.map(customer => customer.id === editingCustomer.id ? newCustomer : customer));
            setEditingCustomer(null);
        } else {
            setCustomers([...customers, { id: Date.now(), ...newCustomer }]);
        }
        setNewCustomer({ name: '', email: '' });
    };

    const handleEdit = (customer) => {
        setNewCustomer(customer);
        setEditingCustomer(customer);
    };

    const handleDelete = (id) => {
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    return (
        <div>
            <h1>Customer Management</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="name"
                    value={newCustomer.name}
                    onChange={handleInputChange}
                    placeholder="Customer Name"
                    required
                />
                <input
                    type="email"
                    name="email"
                    value={newCustomer.email}
                    onChange={handleInputChange}
                    placeholder="Customer Email"
                    required
                />
                <button type="submit">{editingCustomer ? 'Update' : 'Add'}</button>
            </form>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email}
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