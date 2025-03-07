```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    useEffect(() => {
        // Fetching initial customer data (mock API call)
        const initialCustomers = [
            { id: 1, name: 'John Doe', email: 'john@example.com' },
            { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
        ];
        setCustomers(initialCustomers);
    }, []);

    const addCustomer = () => {
        if (newCustomer.name && newCustomer.email) {
            setCustomers([...customers, { id: Date.now(), ...newCustomer }]);
            setNewCustomer({ name: '', email: '' });
        }
    };

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h2>Customer Management</h2>
            <input
                type="text"
                placeholder="Search Customers"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            <div>
                {filteredCustomers.map(customer => (
                    <div key={customer.id}>
                        <h3>{customer.name}</h3>
                        <p>{customer.email}</p>
                    </div>
                ))}
            </div>
            <input
                type="text"
                placeholder="Name"
                value={newCustomer.name}
                onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })}
            />
            <input
                type="email"
                placeholder="Email"
                value={newCustomer.email}
                onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })}
            />
            <button onClick={addCustomer}>Add Customer</button>
        </div>
    );
};

export default CustomerManagement;
```