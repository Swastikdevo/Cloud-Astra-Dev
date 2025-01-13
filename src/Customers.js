```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCustomers = async () => {
            setLoading(true);
            try {
                const response = await fetch('/api/customers');
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                setCustomers(data);
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };
        fetchCustomers();
    }, []);

    if (loading) return <p>Loading customers...</p>;
    if (error) return <p>Error loading customers: {error.message}</p>;

    return (
        <ul>
            {customers.map(customer => (
                <li key={customer.id}>
                    {customer.name} - {customer.email}
                </li>
            ))}
        </ul>
    );
};

export default CustomerList;
```