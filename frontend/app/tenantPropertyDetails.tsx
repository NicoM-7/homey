import React, { useEffect, useState } from "react";
import {
    View,
    Text,
    StyleSheet,
    Image,
    TouchableOpacity,
    ActivityIndicator,
    Alert,
    Linking,
    FlatList,
} from "react-native";
import { useNavigation, useRoute, RouteProp } from "@react-navigation/native";
import { StackNavigationProp } from "@react-navigation/stack";
import useAxios from "./hooks/useAxios";
import { TenantHomeStackParamList } from "./stacks/tenantHomeStack";
import useUser from "./hooks/useUser";
import { Ionicons } from "@expo/vector-icons";
import Button from "./components/button";

type PropertyDetailsRouteProp = RouteProp<TenantHomeStackParamList, "propertyDetails">;
type PropertyDetailsNavigationProp = StackNavigationProp<TenantHomeStackParamList, "propertyDetails">;

export default function TenantPropertyDetailsScreen() {
    const route = useRoute<PropertyDetailsRouteProp>();
    const navigation = useNavigation<PropertyDetailsNavigationProp>();
    const { get, error } = useAxios();
    const { user, userLoading, userError } = useUser();

    const property = route.params.property;

    const [images, setImages] = useState<any[]>([]);
    const [loadingImages, setLoadingImages] = useState(true);
    const [landlordRating, setLandlordRating] = useState<string>("N/A");
    const [propertyRating, setPropertyRating] = useState<string>("N/A");

    useEffect(() => {
        fetchPropertyImages();
        fetchLandlordRating();
        fetchPropertyRating();
    }, []);

    useEffect(() => {
        if (error) {
            Alert.alert("Error", error);
        }
    }, [error]);

    const fetchPropertyImages = async () => {
        try {
            const response = await get<any>(`/api/properties/${property.id}/images`);
            if (response) {
                setImages(response.data);
            }
        } catch (error) {
            Alert.alert("Error", "Failed to load property images.");
        } finally {
            setLoadingImages(false);
        }
    };

    const fetchLandlordRating = async () => {
        try {
            const response = await get<any>("/api/reviews/", { reviewType: "user", reviewedItemId: property.landlord.id });
            if (response && response.data.length > 0) {
                let sum = 0;
                response.data.forEach((review: any) => {
                    sum += review.score;
                });
                const avg = (sum / response.data.length).toFixed(1);
                setLandlordRating(avg);
            } else {
                setLandlordRating("N/A");
            }
        } catch (err) {
            setLandlordRating("N/A");
        }
    };

    const fetchPropertyRating = async () => {
        try {
            const response = await get<any>("/api/reviews/", { reviewType: "property", reviewedItemId: property.id });
            if (response && response.data.length > 0) {
                let sum = 0;
                response.data.forEach((review: any) => {
                    sum += review.score;
                });
                const avg = (sum / response.data.length).toFixed(1);
                setPropertyRating(avg);
            } else {
                setPropertyRating("N/A");
            }
        } catch (err) {
            setPropertyRating("N/A");
        }
    };

    const handleEmailLandlord = () => {
        if (!property.landlord?.email) return;
        const subject = encodeURIComponent(`Inquiry about ${property.name}`);
        const body = encodeURIComponent(
            `Hello ${property.landlord.firstName},\n\nI'm interested in your property at ${property.address}. Can we schedule a time to discuss?\n\nBest regards,\n${user.firstName} ${user.lastName}`
        );
        Linking.openURL(`mailto:${property.landlord.email}?subject=${subject}&body=${body}`);
    };

    if (userLoading) return <ActivityIndicator size="large" color="#0000ff" />;
    if (userError) return <Text>Error: {userError}</Text>;
    if (!user) return <Text>No user found.</Text>;

    return (
        <View style={styles.root}>
            {/* Sticky Header */}
            <View style={styles.header}>
                <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
                    <Ionicons name="arrow-back" size={24} color="black" />
                </TouchableOpacity>
                <Text style={styles.headerText}>{property.name}</Text>
            </View>

            <FlatList
                ListHeaderComponent={
                    <>
                        {/* Property Details Section */}
                        <View style={styles.section}>
                            <Text style={styles.sectionTitle}>Property Details</Text>
                            <Text style={styles.detailText}>🏠 {property.propertyType}</Text>
                            <Text style={styles.detailText}>
                                📍 {property.address}, {property.city}
                            </Text>
                            <Text style={styles.detailText}>💰 ${property.price} / month</Text>
                            <Text style={styles.detailText}>🛏 {property.bedrooms} Bedroom(s)</Text>
                            <Text style={styles.description}>{property.description}</Text>
                            {/* House Rating Field */}
                            <TouchableOpacity
                                style={styles.reviewButton}
                                onPress={() =>
                                    navigation.navigate("allReviews", { reviewType: "property", itemId: property.id })
                                }
                            >
                                <Text style={[styles.detailText, styles.ratingText]}>
                                    ⭐ {propertyRating} / 5.0
                                </Text>
                                <Ionicons name="chevron-forward" size={20} color="gray" style={{ marginLeft: 5 }} />
                            </TouchableOpacity>

                        </View>

                        {/* Landlord Contact Section */}
                        <View style={styles.section}>
                            <Text style={styles.sectionTitle}>Landlord Contact</Text>
                            <Text style={styles.detailText}>
                                👤 {property.landlord.firstName} {property.landlord.lastName}
                            </Text>
                            <Text style={styles.detailText}>📧 {property.landlord.email}</Text>
                            {/* Landlord Rating Field */}
                            <TouchableOpacity
                                style={styles.reviewButton}
                                onPress={() =>
                                    navigation.navigate("allReviews", { reviewType: "user", itemId: property.landlord.id })
                                }
                            >
                                <Text style={[styles.detailText, styles.ratingText]}>
                                    ⭐ {landlordRating} / 5.0
                                </Text>
                                <Ionicons name="chevron-forward" size={20} color="gray" style={{ marginLeft: 5 }} />
                            </TouchableOpacity>

                            <Button
                                text="Contact Landlord"
                                onClick={handleEmailLandlord}
                                customStyle={{
                                    buttonStyle: { backgroundColor: "#4CAF50" },
                                    textStyle: { color: "white" },
                                }}
                            />
                        </View>

                        {/* Property Image Gallery */}
                        <Text style={[styles.sectionTitle, styles.imageSectionTitle]}>Property Images</Text>
                    </>
                }
                data={loadingImages ? [] : images}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) => (
                    <View style={styles.imageCard}>
                        {item.label && <Text style={styles.imageLabel}>{item.label}</Text>}
                        <Image source={{ uri: item.image }} style={styles.propertyImage} />
                        {item.description && <Text style={styles.imageDescription}>{item.description}</Text>}
                    </View>
                )}
                ListEmptyComponent={
                    loadingImages ? (
                        <ActivityIndicator size="large" color="#0000ff" />
                    ) : (
                        <Text style={styles.noImagesText}>No images available.</Text>
                    )
                }
            />
        </View>
    );
}

const styles = StyleSheet.create({
    root: {
        flex: 1,
        backgroundColor: "#f5f5f5",
    },
    header: {
        flexDirection: "row",
        alignItems: "center",
        paddingTop: 50,
        paddingBottom: 10,
        backgroundColor: "white",
        borderBottomWidth: 1,
        borderBottomColor: "#ddd",
        elevation: 3,
        zIndex: 100,
    },
    backButton: {
        paddingLeft: 15,
    },
    headerText: {
        fontSize: 22,
        fontWeight: "bold",
        flex: 1,
        textAlign: "center",
        paddingRight: 35,
    },
    reviewButton: {
        flexDirection: "row",
        alignItems: "center",
    },
    section: {
        backgroundColor: "white",
        padding: 20,
        borderRadius: 8,
        elevation: 3,
        marginBottom: 20,
        marginHorizontal: 16,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: "bold",
        marginBottom: 10,
    },
    imageSectionTitle: {
        marginHorizontal: 16,
    },
    detailText: {
        fontSize: 16,
        marginBottom: 5,
    },
    ratingText: {
        color: "#FFA500",
    },
    description: {
        fontSize: 14,
        color: "#555",
        marginTop: 10,
        lineHeight: 20,
    },
    propertyImage: {
        width: "100%",
        height: 300,
        borderRadius: 8,
    },
    imageCard: {
        marginBottom: 20,
        backgroundColor: "#fff",
        padding: 10,
        borderRadius: 8,
        elevation: 3,
        marginHorizontal: 16,
    },
    imageLabel: {
        fontSize: 16,
        fontWeight: "bold",
        marginBottom: 5,
        textAlign: "center",
    },
    imageDescription: {
        marginTop: 5,
        fontSize: 14,
        color: "#555",
        textAlign: "center",
    },
    noImagesText: {
        fontSize: 14,
        color: "#999",
        textAlign: "center",
        marginTop: 10,
    },
});
