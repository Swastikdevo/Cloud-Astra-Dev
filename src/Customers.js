```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
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
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchCustomers();
    }, []);
  
    const deleteCustomer = async (id) => {
        try {
            await fetch(`/api/customers/${id}`, { method: 'DELETE' });
            setCustomers(customers.filter(customer => customer.id !== id));
        } catch (err) {
            setError(err.message);
        }
    };
  
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
  
    return (
        <div>
            <h1>Customer Management</h1>
            <ul>
                {customers.map(customer => (
                    <li key={customer.id}>
                        {customer.name}
                        <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```