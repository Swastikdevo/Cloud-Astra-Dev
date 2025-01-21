```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCustomers = async () => {
            try {
                const response = await fetch('/api/customers');
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                setCustomers(data);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };
        fetchCustomers();
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            <h2>Customer List</h2>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name} - {customer.email}
                    </li>
                ))}
            </ul>
        </div>
    );
};

const CustomerManagement = () => {
    const [isAdding, setIsAdding] = useState(false);
    const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewCustomer(prev => ({ ...prev, [name]: value }));
    };

    const handleAddCustomer = async (e) => {
        e.preventDefault();
        const response = await fetch('/api/customers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer)
        });
        if (response.ok) {
            setNewCustomer({ name: '', email: '' });
            setIsAdding(false);
        }
    };

    return (
        <div>
            <CustomerList />
            {isAdding ? (
                <form onSubmit={handleAddCustomer}>
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
                    <button type="submit">Add Customer</button>
                    <button type="button" onClick={() => setIsAdding(false)}>Cancel</button>
                </form>
            ) : (
                <button onClick={() => setIsAdding(true)}>Add New Customer</button>
            )}
        </div>
    );
};

export default CustomerManagement;
```