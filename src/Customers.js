```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        // Simulate fetching customers from an API
        const fetchedCustomers = [
            { id: 1, name: 'John Doe', email: 'john@example.com' },
            { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
        ];
        setCustomers(fetchedCustomers);
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewCustomer({ ...newCustomer, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setCustomers([...customers, { id: customers.length + 1, ...newCustomer }]);
        setNewCustomer({ name: '', email: '' });
    };

    const handleDelete = (id) => {
        setCustomers(customers.filter(customer => customer.id !== id));
    };

    return (
        <div>
            <h2>Customer Management</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" value={newCustomer.name} onChange={handleChange} placeholder="Customer Name" required />
                <input type="email" name="email" value={newCustomer.email} onChange={handleChange} placeholder="Customer Email" required />
                <button type="submit">Add Customer</button>
            </form>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email}
                        <button onClick={() => handleDelete(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```