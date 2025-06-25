--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: enum_Conversations_type; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public."enum_Conversations_type" AS ENUM (
    'dm',
    'group'
);


ALTER TYPE public."enum_Conversations_type" OWNER TO admin;

--
-- Name: enum_Participants_role; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public."enum_Participants_role" AS ENUM (
    'tenant',
    'landlord'
);


ALTER TYPE public."enum_Participants_role" OWNER TO admin;

--
-- Name: enum_Profiles_cleaningHabits; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public."enum_Profiles_cleaningHabits" AS ENUM (
    '',
    'Low',
    'Medium',
    'High'
);


ALTER TYPE public."enum_Profiles_cleaningHabits" OWNER TO admin;

--
-- Name: enum_Profiles_noiseLevel; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public."enum_Profiles_noiseLevel" AS ENUM (
    '',
    'Low',
    'Medium',
    'High'
);


ALTER TYPE public."enum_Profiles_noiseLevel" OWNER TO admin;

--
-- Name: enum_Reviews_reviewType; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public."enum_Reviews_reviewType" AS ENUM (
    'user',
    'property'
);


ALTER TYPE public."enum_Reviews_reviewType" OWNER TO admin;

--
-- Name: enum_Users_role; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public."enum_Users_role" AS ENUM (
    'admin',
    'landlord',
    'tenant'
);


ALTER TYPE public."enum_Users_role" OWNER TO admin;

--
-- Name: enum_properties_propertyType; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public."enum_properties_propertyType" AS ENUM (
    'House',
    'Apartment',
    'Condo',
    'Townhouse',
    'Duplex',
    'Studio',
    'Loft',
    'Bungalow',
    'Cabin',
    'Mobile Home',
    'Other'
);


ALTER TYPE public."enum_properties_propertyType" OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: CalendarEvents; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."CalendarEvents" (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    "eventDate" date NOT NULL,
    "startTime" time without time zone,
    "endTime" time without time zone,
    location character varying(255),
    description text,
    "groupId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "userId" integer
);


ALTER TABLE public."CalendarEvents" OWNER TO admin;

--
-- Name: CalendarEvents_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."CalendarEvents_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."CalendarEvents_id_seq" OWNER TO admin;

--
-- Name: CalendarEvents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."CalendarEvents_id_seq" OWNED BY public."CalendarEvents".id;


--
-- Name: Chores; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Chores" (
    id integer NOT NULL,
    "choreName" character varying(255) NOT NULL,
    room character varying(255) NOT NULL,
    "assignedTo" integer,
    completed boolean DEFAULT false,
    "bannerImage" character varying(255),
    "dueDate" timestamp with time zone NOT NULL,
    "groupId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Chores" OWNER TO admin;

--
-- Name: Chores_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Chores_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Chores_id_seq" OWNER TO admin;

--
-- Name: Chores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Chores_id_seq" OWNED BY public."Chores".id;


--
-- Name: Conversations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Conversations" (
    id integer NOT NULL,
    "groupId" integer NOT NULL,
    type public."enum_Conversations_type" NOT NULL,
    name character varying(255),
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Conversations" OWNER TO admin;

--
-- Name: Conversations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Conversations_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Conversations_id_seq" OWNER TO admin;

--
-- Name: Conversations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Conversations_id_seq" OWNED BY public."Conversations".id;


--
-- Name: Inventories; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Inventories" (
    "itemId" integer NOT NULL,
    "itemName" character varying(255) NOT NULL,
    quantity integer NOT NULL,
    "groupId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Inventories" OWNER TO admin;

--
-- Name: Inventories_itemId_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Inventories_itemId_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Inventories_itemId_seq" OWNER TO admin;

--
-- Name: Inventories_itemId_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Inventories_itemId_seq" OWNED BY public."Inventories"."itemId";


--
-- Name: Items; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Items" (
    "itemId" integer NOT NULL,
    "listId" integer NOT NULL,
    item character varying(255) NOT NULL,
    "assignedTo" character varying(255),
    purchased integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Items" OWNER TO admin;

--
-- Name: Items_itemId_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Items_itemId_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Items_itemId_seq" OWNER TO admin;

--
-- Name: Items_itemId_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Items_itemId_seq" OWNED BY public."Items"."itemId";


--
-- Name: Lists; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Lists" (
    "listId" integer NOT NULL,
    "userId" integer NOT NULL,
    "listName" character varying(255) NOT NULL,
    "groupId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Lists" OWNER TO admin;

--
-- Name: Lists_listId_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Lists_listId_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Lists_listId_seq" OWNER TO admin;

--
-- Name: Lists_listId_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Lists_listId_seq" OWNED BY public."Lists"."listId";


--
-- Name: Messages; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Messages" (
    id integer NOT NULL,
    "conversationId" integer NOT NULL,
    "senderId" integer NOT NULL,
    content text NOT NULL,
    "readBy" json,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Messages" OWNER TO admin;

--
-- Name: Messages_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Messages_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Messages_id_seq" OWNER TO admin;

--
-- Name: Messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Messages_id_seq" OWNED BY public."Messages".id;


--
-- Name: Participants; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Participants" (
    id integer NOT NULL,
    "conversationId" integer NOT NULL,
    "userId" integer NOT NULL,
    role public."enum_Participants_role" DEFAULT 'tenant'::public."enum_Participants_role",
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Participants" OWNER TO admin;

--
-- Name: Participants_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Participants_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Participants_id_seq" OWNER TO admin;

--
-- Name: Participants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Participants_id_seq" OWNED BY public."Participants".id;


--
-- Name: Profiles; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Profiles" (
    id integer NOT NULL,
    "cleaningHabits" public."enum_Profiles_cleaningHabits",
    "noiseLevel" public."enum_Profiles_noiseLevel",
    "sleepStart" character varying(255),
    "sleepEnd" character varying(255),
    alergies character varying(255),
    "userId" integer NOT NULL,
    "groupId" integer NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Profiles" OWNER TO admin;

--
-- Name: Profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Profiles_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Profiles_id_seq" OWNER TO admin;

--
-- Name: Profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Profiles_id_seq" OWNED BY public."Profiles".id;


--
-- Name: Reviews; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Reviews" (
    "reviewId" integer NOT NULL,
    "reviewType" public."enum_Reviews_reviewType" NOT NULL,
    "reviewedItemId" integer NOT NULL,
    "reviewerId" integer NOT NULL,
    score integer NOT NULL,
    description character varying(255),
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Reviews" OWNER TO admin;

--
-- Name: Reviews_reviewId_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Reviews_reviewId_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Reviews_reviewId_seq" OWNER TO admin;

--
-- Name: Reviews_reviewId_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Reviews_reviewId_seq" OWNED BY public."Reviews"."reviewId";


--
-- Name: Users; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."Users" (
    id integer NOT NULL,
    "firstName" character varying(255) NOT NULL,
    "lastName" character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    role public."enum_Users_role" NOT NULL,
    verified boolean DEFAULT false,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Users" OWNER TO admin;

--
-- Name: Users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."Users_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Users_id_seq" OWNER TO admin;

--
-- Name: Users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."Users_id_seq" OWNED BY public."Users".id;


--
-- Name: expenses; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.expenses (
    id integer NOT NULL,
    "expenseName" character varying(255) NOT NULL,
    "groupId" integer NOT NULL,
    amount double precision NOT NULL,
    "paidBy" integer NOT NULL,
    "owedTo" integer NOT NULL,
    completed boolean DEFAULT false NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.expenses OWNER TO admin;

--
-- Name: expenses_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.expenses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.expenses_id_seq OWNER TO admin;

--
-- Name: expenses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.expenses_id_seq OWNED BY public.expenses.id;


--
-- Name: group_participants; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.group_participants (
    id integer NOT NULL,
    "groupId" integer NOT NULL,
    "tenantId" integer NOT NULL,
    "joinedAt" timestamp with time zone
);


ALTER TABLE public.group_participants OWNER TO admin;

--
-- Name: group_participants_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.group_participants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.group_participants_id_seq OWNER TO admin;

--
-- Name: group_participants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.group_participants_id_seq OWNED BY public.group_participants.id;


--
-- Name: groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    "landlordId" integer NOT NULL,
    "propertyId" integer,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.groups OWNER TO admin;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.groups_id_seq OWNER TO admin;

--
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


--
-- Name: properties; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.properties (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    address character varying(255) NOT NULL,
    city character varying(255) NOT NULL,
    "propertyDescription" text NOT NULL,
    bedrooms integer NOT NULL,
    price integer NOT NULL,
    "propertyType" public."enum_properties_propertyType" NOT NULL,
    availability boolean DEFAULT true NOT NULL,
    "landlordId" integer NOT NULL,
    "exteriorImage" bytea NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.properties OWNER TO admin;

--
-- Name: properties_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.properties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.properties_id_seq OWNER TO admin;

--
-- Name: properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.properties_id_seq OWNED BY public.properties.id;


--
-- Name: property_images; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.property_images (
    id integer NOT NULL,
    "propertyId" integer NOT NULL,
    label character varying(255) NOT NULL,
    image bytea NOT NULL,
    description text,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.property_images OWNER TO admin;

--
-- Name: property_images_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.property_images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.property_images_id_seq OWNER TO admin;

--
-- Name: property_images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.property_images_id_seq OWNED BY public.property_images.id;


--
-- Name: stores; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.stores (
    "itemID" integer NOT NULL,
    "itemName" character varying(255),
    store character varying(255) NOT NULL,
    price character varying(255) NOT NULL,
    "storeLink" character varying(255) NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.stores OWNER TO admin;

--
-- Name: stores_itemID_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public."stores_itemID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."stores_itemID_seq" OWNER TO admin;

--
-- Name: stores_itemID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public."stores_itemID_seq" OWNED BY public.stores."itemID";


--
-- Name: CalendarEvents id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."CalendarEvents" ALTER COLUMN id SET DEFAULT nextval('public."CalendarEvents_id_seq"'::regclass);


--
-- Name: Chores id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Chores" ALTER COLUMN id SET DEFAULT nextval('public."Chores_id_seq"'::regclass);


--
-- Name: Conversations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Conversations" ALTER COLUMN id SET DEFAULT nextval('public."Conversations_id_seq"'::regclass);


--
-- Name: Inventories itemId; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Inventories" ALTER COLUMN "itemId" SET DEFAULT nextval('public."Inventories_itemId_seq"'::regclass);


--
-- Name: Items itemId; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Items" ALTER COLUMN "itemId" SET DEFAULT nextval('public."Items_itemId_seq"'::regclass);


--
-- Name: Lists listId; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Lists" ALTER COLUMN "listId" SET DEFAULT nextval('public."Lists_listId_seq"'::regclass);


--
-- Name: Messages id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Messages" ALTER COLUMN id SET DEFAULT nextval('public."Messages_id_seq"'::regclass);


--
-- Name: Participants id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Participants" ALTER COLUMN id SET DEFAULT nextval('public."Participants_id_seq"'::regclass);


--
-- Name: Profiles id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Profiles" ALTER COLUMN id SET DEFAULT nextval('public."Profiles_id_seq"'::regclass);


--
-- Name: Reviews reviewId; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Reviews" ALTER COLUMN "reviewId" SET DEFAULT nextval('public."Reviews_reviewId_seq"'::regclass);


--
-- Name: Users id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users" ALTER COLUMN id SET DEFAULT nextval('public."Users_id_seq"'::regclass);


--
-- Name: expenses id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.expenses ALTER COLUMN id SET DEFAULT nextval('public.expenses_id_seq'::regclass);


--
-- Name: group_participants id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.group_participants ALTER COLUMN id SET DEFAULT nextval('public.group_participants_id_seq'::regclass);


--
-- Name: groups id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


--
-- Name: properties id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.properties ALTER COLUMN id SET DEFAULT nextval('public.properties_id_seq'::regclass);


--
-- Name: property_images id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.property_images ALTER COLUMN id SET DEFAULT nextval('public.property_images_id_seq'::regclass);


--
-- Name: stores itemID; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.stores ALTER COLUMN "itemID" SET DEFAULT nextval('public."stores_itemID_seq"'::regclass);


--
-- Name: CalendarEvents CalendarEvents_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."CalendarEvents"
    ADD CONSTRAINT "CalendarEvents_pkey" PRIMARY KEY (id);


--
-- Name: Chores Chores_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Chores"
    ADD CONSTRAINT "Chores_pkey" PRIMARY KEY (id);


--
-- Name: Conversations Conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Conversations"
    ADD CONSTRAINT "Conversations_pkey" PRIMARY KEY (id);


--
-- Name: Inventories Inventories_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Inventories"
    ADD CONSTRAINT "Inventories_pkey" PRIMARY KEY ("itemId");


--
-- Name: Items Items_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Items"
    ADD CONSTRAINT "Items_pkey" PRIMARY KEY ("itemId");


--
-- Name: Lists Lists_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Lists"
    ADD CONSTRAINT "Lists_pkey" PRIMARY KEY ("listId", "userId");


--
-- Name: Messages Messages_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Messages"
    ADD CONSTRAINT "Messages_pkey" PRIMARY KEY (id);


--
-- Name: Participants Participants_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Participants"
    ADD CONSTRAINT "Participants_pkey" PRIMARY KEY (id);


--
-- Name: Profiles Profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Profiles"
    ADD CONSTRAINT "Profiles_pkey" PRIMARY KEY (id);


--
-- Name: Reviews Reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Reviews"
    ADD CONSTRAINT "Reviews_pkey" PRIMARY KEY ("reviewId");


--
-- Name: Users Users_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_email_key" UNIQUE (email);


--
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (id);


--
-- Name: Users Users_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_username_key" UNIQUE (username);


--
-- Name: expenses expenses_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT expenses_pkey PRIMARY KEY (id);


--
-- Name: group_participants group_participants_groupId_tenantId_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.group_participants
    ADD CONSTRAINT "group_participants_groupId_tenantId_key" UNIQUE ("groupId", "tenantId");


--
-- Name: group_participants group_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.group_participants
    ADD CONSTRAINT group_participants_pkey PRIMARY KEY (id);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: properties properties_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.properties
    ADD CONSTRAINT properties_pkey PRIMARY KEY (id);


--
-- Name: property_images property_images_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.property_images
    ADD CONSTRAINT property_images_pkey PRIMARY KEY (id);


--
-- Name: stores stores_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY ("itemID");


--
-- Name: CalendarEvents CalendarEvents_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."CalendarEvents"
    ADD CONSTRAINT "CalendarEvents_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: CalendarEvents CalendarEvents_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."CalendarEvents"
    ADD CONSTRAINT "CalendarEvents_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Chores Chores_assignedTo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Chores"
    ADD CONSTRAINT "Chores_assignedTo_fkey" FOREIGN KEY ("assignedTo") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Chores Chores_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Chores"
    ADD CONSTRAINT "Chores_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Conversations Conversations_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Conversations"
    ADD CONSTRAINT "Conversations_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Inventories Inventories_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Inventories"
    ADD CONSTRAINT "Inventories_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Lists Lists_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Lists"
    ADD CONSTRAINT "Lists_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Messages Messages_conversationId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Messages"
    ADD CONSTRAINT "Messages_conversationId_fkey" FOREIGN KEY ("conversationId") REFERENCES public."Conversations"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Messages Messages_senderId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Messages"
    ADD CONSTRAINT "Messages_senderId_fkey" FOREIGN KEY ("senderId") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Participants Participants_conversationId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Participants"
    ADD CONSTRAINT "Participants_conversationId_fkey" FOREIGN KEY ("conversationId") REFERENCES public."Conversations"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Participants Participants_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Participants"
    ADD CONSTRAINT "Participants_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Profiles Profiles_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."Profiles"
    ADD CONSTRAINT "Profiles_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: expenses expenses_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT "expenses_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: expenses expenses_owedTo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT "expenses_owedTo_fkey" FOREIGN KEY ("owedTo") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: expenses expenses_paidBy_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT "expenses_paidBy_fkey" FOREIGN KEY ("paidBy") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: group_participants group_participants_groupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.group_participants
    ADD CONSTRAINT "group_participants_groupId_fkey" FOREIGN KEY ("groupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: group_participants group_participants_tenantId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.group_participants
    ADD CONSTRAINT "group_participants_tenantId_fkey" FOREIGN KEY ("tenantId") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: groups groups_landlordId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT "groups_landlordId_fkey" FOREIGN KEY ("landlordId") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: groups groups_propertyId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT "groups_propertyId_fkey" FOREIGN KEY ("propertyId") REFERENCES public.properties(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: properties properties_landlordId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.properties
    ADD CONSTRAINT "properties_landlordId_fkey" FOREIGN KEY ("landlordId") REFERENCES public."Users"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: property_images property_images_propertyId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.property_images
    ADD CONSTRAINT "property_images_propertyId_fkey" FOREIGN KEY ("propertyId") REFERENCES public.properties(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

